# Function to schedule an event on Google Calendar
def schedule_event(calendar_service, event):
    created_event = (
        calendar_service.events()
        .insert(calendarId='chansoosong@gmail.com', body=event)
        .execute()
    )
    return created_event
