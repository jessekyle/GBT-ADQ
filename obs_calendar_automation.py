"""
Prerequistites:
- bs4/ beautifulsoup
- Twilio library
- Download client_secret.json file and put it in same directory

- Program created by Isabel Angelo.
- Installed on GBT headnode on Feb 2017, cron job installed 4x per day.
- print to screen lines removed.
- added entry to SQL database

-To do:
  Add in Twillio to Howard's phone.
  Consider posting future targetlist to UC Berkeley SETI website.
  Run summary keyword on targetlist creation program and post that to website as well.
      -perhaps make the summary list a weekly cron job.

"""
from quickstart import *
from gbt_scraper import *
import time
import copy
import sys
from twilio.rest import TwilioRestClient
import MySQLdb 

# Open connection to SQL server and a cursor
db = MySQLdb.connect("","","","BLtargets" )
cursor = db.cursor()


def start_time(scraped_event):
	''' gets start time of an event scraped GBT events list'''
	e = scraped_event.start[:10]+'T'+event.start[11:]+':00Z'
	e = e.decode('unicode_escape')
	return e

def end_time(scraped_event):
	''' gets start time of an event scraped GBT events list '''
	e = scraped_event.end[:10]+'T'+event.end[11:]+':00Z'
	e = e.decode('unicode_escape')
	return e

class Event:
	'''Class for storing information about existing Google Calendar Events'''
	def __init__(self, summary= None, start=None, end=None, link=None):
		self.summary = summary
		self.start = start
		self.end = end
		self.link = link

def get_events(existing_events = []):
    '''
    get list of existing events on google calendar
    'eventlist: list stores information about each event on calendar
    returns: list containing start times of events on calendar '''
    now = datetime.datetime.utcnow() # 'Z' indicates UTC time
    then= datetime.datetime.utcnow()-datetime.timedelta(7)
    t = then.isoformat() + 'Z'
    eventsResult = service.events().list(
        calendarId=cal['id'], timeMin=t, maxResults=100, singleEvents=True,
        orderBy='startTime', timeZone = 'Etc/UTC').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for e in events:
        e1 = e['summary']
        e2 = e['start'].get('dateTime', e['start'].get('date'))
        e3 = e['end'].get('dateTime', e['start'].get('date'))
        e4 = e.get('htmlLink')
        existing_events.append(Event(summary = e1, start = e2, end = e3, link  = e4 ))

def check_if_exists(scraped_event):
	#make it so that it only checks for existing GBT events
	''' check to see if an event from scraper is already on calendar
	returns True if exists, False if doesn't '''
	if start_time(scraped_event) in existing_start_times:
		print 'Event Exists'
		return True
	elif end_time(scraped_event) in existing_end_times:
		print 'Event Exists'
		return True
	else:
		print 'Event Does Not Exist, Updating New Event'
		return False
		
def add_event(scraped_event):
	''' adds event to google calendar '''
	event_start = str(start_time(scraped_event))[:-1]
	event_end = str(end_time(scraped_event))[:-1]
	event = {
      'summary': 'GBT Observing '+ scraped_event.receivers +'band',
      'location': '',
      'description': '',
      'start': {
        'dateTime': event_start,
        'timeZone': 'Etc/UTC',
      },
      'end': {
        'dateTime': event_end,
        'timeZone': 'Etc/UTC',
      },
      'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=1'
      ],
	#'attendees': [
    #	{'email': 'isabelangelo@berkeley.edu'},
    #	{'email': 'hisaacson@berkeley.edu'},
  	#],
    }
	try:
		event = service.events().insert(calendarId=cal['id'], body=event).execute()
		print 'Event created: %s' % (event.get('htmlLink'))
		print 'begin: ',event_start
		print 'end:   ',event_end 
	except Exception as e:
		pass

	
def write_to_database(scraped_event):
	'''writes the event date, time, timezone and duration to database
 	gbt_observations_database.txt '''
	s = start_time(scraped_event)
	a = time.strptime(str(start_time(scraped_event)), '%Y-%m-%dT%H:%M:%SZ')
	b = time.strptime(str(end_time(scraped_event)), '%Y-%m-%dT%H:%M:%SZ')
	
	a = time.mktime(a)
	b = time.mktime(b)
	
	d = b - a
	
	days = int(d) / 86400
	hours = str(int(d) / 3600 % 24)
	minutes = str(int(d) / 60 % 60)
	seconds = str(int(d) % 60)
	
	duration = hours + 'h' + minutes + 'm' + seconds + 's'
	duration_sql = float(hours)  + float(minutes)/60. + float(seconds)/3600.
	entry =  s[:10]+ '\t' + s[11:-1] + '\t' + 'UTC' + '\t' + duration + '\n'
	
	print "Writing to database file"
	with open('/home/obs/calendar/my_version_of_googleAPI/gbt_observations_database.txt', 'a') as file:
		file.write(entry)
	print 'database updated'
	return duration_sql

def send_text(new_event, hours):
	'''
	send message if event is 4 hours ahead and unclaimed:
	'''
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
	client.messages.create( 
		to = '+12134478172', 
    	from_ = '+12138631121',
    	body = 'Upcoming Observing Event in ' + str(hours) + ' hours\n'
    		'claim at:'+ new_event.link,
		)
	#print 'Observers Notified'
		
def format4sql(unq_events,duration):
	sql_strt = unq_events.start
	sql_com = """ INSERT INTO gb_observations (id,start,length_hrs,billed_hrs)
                      VALUES (NULL,'"""+sql_strt+"',"+str(duration)+','+str(duration)+');'
	return sql_com

#get event list from GBT website
scraper = GBTScraper(date=time.strftime("%m/%d/%Y"), days = 30) #store for next 30 days
scraper.make(t = 'utc')
scraped_events = scraper.btlpSchedule

#get credentials and calendar list from Google Calendar
credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('calendar', 'v3', http=http)
page_token = None
BL_CAL = 'BL_Obs'
while True:
  calendar_list = service.calendarList().list(pageToken=page_token).execute()
  for calendar_list_entry in calendar_list['items']: #hti
    #print 'calendar name:',calendar_list_entry['summary'] #hti
    if calendar_list_entry['summary'] == BL_CAL:
      cal = calendar_list_entry# ['items']
      #print 'credentials successful, calendar retrieved'
      break
  page_token = calendar_list.get('nextPageToken')
  if not page_token:
    break
#cal = calendar_list['items'][2] #comment this out unless you are using the test calendar


#store existing events on Google Calendar
existing_events = []
get_events(existing_events)

#store their start and end times for check)if_exists function
existing_start_times = [] #storing existing start times
existing_end_times = [] #storing existing end times
for ev in existing_events:
	#only append events with 'GBT' contained in the summary to avoid Parkes!!!
    existing_start_times.append(ev.start)
    existing_end_times.append(ev.end)


# Merge back-to-back events before adding to calendar
# print ''
# print 'Checking for back to back events...'

unq_events = []

for i in range(len(scraped_events)):
	#print 'Event ',i,':',
	event = scraped_events[i]
	#Reset back2back for each event
	back2back = False
	for other_event in scraped_events:
		#this if statement extends first two events
		if event.end == other_event.start:
			#print 'Back to back detected, events merged' 
			back2back = True
			unq_events.append(copy.copy(event))
			unq_events[-1].end = other_event.end
		# Removes 2nd of two events
		elif event.start == other_event.end:
			back2back = True
			#print 'Back to back detected, removing 2nd of back to back events'
	# Allow single events to be added
	if back2back == False:
		unq_events.append(event)
		print 'Adding in single event'
		

#add unique events to calendar and write to database
print 'Total Unique Events:', len(unq_events)

#print ''
#print 'Checking if events exist...'

for i in range(len(unq_events)):
	print 'Unique Event',i,':',
	event = unq_events[i]
	if check_if_exists(event) == False:
		add_event(event)
		duration = write_to_database(event)
		sql_com  = format4sql(event,duration)
		cursor.execute(sql_com)
		# Add entry to SQL database
	else:
		print " Not writing to database nor text file"
		#print event

#notify people if any events are in <4 hours
all_events = []
get_events(all_events)
#all_events=all_events[:2] #Kludge
upcoming_events = 0
unclaimed_events = 0
for ev in all_events:
    #get event time
    # exclude events that are "observer on call". Identify by date stamp of allday events
    if len(ev.start) != 10:
       now = datetime.datetime.utcnow()
       a = time.strptime(now.isoformat()[:-7]+'Z', '%Y-%m-%dT%H:%M:%SZ') #current time
       b = time.strptime(ev.start, '%Y-%m-%dT%H:%M:%SZ') #time of event
       #convert times to float
       a = time.mktime(a) 
       b = time.mktime(b)
       #compute and store difference
       d = b-a
       if d > 0:
          hours = int(d) / 3600 % 24
          if 0 < hours < 4:
			#print 'Upcoming Event Detected in ' + str(hours) + ' hours' 
			upcoming_events += 1
			if ev.summary[:16] == 'Parkes Observing':
				#print 'Event Unclaimed, Observers Notified'
				#send_text(ev, hours)
				unclaimed_events += 1

if upcoming_events == 0:
	print 'No Upcoming Events Detected'

# Commit to sql database and Close
db.commit()
db.close()


