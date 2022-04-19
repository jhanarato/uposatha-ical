import asyncio
import desktop_notify

async def show_notifcation():
	import icalendar
	from forest_sangha_moons import MahanikayaCalendar

	with open("../mahanikaya.ical", "r") as f:
		content = f.read()

	ical = icalendar.Calendar.from_ical(content)
	calendar = MahanikayaCalendar()
	calendar.import_ical(ical)

	next_uposatha = calendar.next_uposatha()
	days = calendar.days_to_next_uposatha()
	if days == 1:
		summary = "Uposatha Tomorrow"
	else:
		summary = "Uposatha in {} days".format(days)

	body = "{} moon {}".format(
		next_uposatha.moon_name,
		next_uposatha.date.strftime("%A, %d/%m")
	)

	notify = desktop_notify.aio.Notify(summary, body)
	await notify.show()

asyncio.run(show_notifcation())
