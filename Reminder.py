from helper import are_valid_hours, are_valid_minutes, remove_extra_spaces
from storage import save, load
from apscheduler.triggers.cron import CronTrigger


class Reminder:

    def load_reminders(self, key):
        return load(key) or []

    def add_reminder(self, user_id, content, hh, mm, foo, scheduler, daily=True):
        if remove_extra_spaces(content) == "":
            return "Nothing to remind"
        if not are_valid_hours(hh):
            return "Hours are not valid"
        if not are_valid_minutes(mm):
            return "Minutes are not valid"

        previous_reminders = self.load_reminders(user_id)
        reminder = {"hh": str(hh), "mm": str(mm), "content": str(
            content), "job_id": str(len(previous_reminders)+1), "daily": daily}
        previous_reminders.append(reminder)
        is_saved = save(user_id, previous_reminders)
        trigger = CronTrigger(year="*", month="*", day="*",
                              hour=hh, minute=mm, second="0")

        job_id = len(previous_reminders)
        job_id = str(job_id)
        job_id = f"{user_id}-{job_id}"
        scheduler.add_job(foo,
                          trigger=trigger,
                          args=[user_id, content, job_id, daily],
                          id=job_id)
        return "Reminder saved" if is_saved else "Problem setting the reminder"

    def get_reminders(self, user_id):
        previous_reminders = self.load_reminders(user_id)
        response_string = "No Reminders"
        if len(previous_reminders) > 0:
            response_string = ""
            for id, reminder in enumerate(previous_reminders):
                response_string = response_string + \
                    str(id+1)+". "+reminder["content"] + \
                    " at "+reminder["hh"]+":"+reminder["mm"]
                if not reminder["daily"]:
                    response_string = f"{response_string} (One-Time)"
                response_string = response_string+"\n"

        return response_string

    def get_reminder_by_id(self, user_id, reminder_id):
        previous_reminders = self.load_reminders(user_id)
        if reminder_id < len(previous_reminders):
            return previous_reminders[reminder_id]

    def delete_reminder(self, user_id, reminder_id, scheduler):

        if reminder_id.isdigit():
            reminder_id = int(reminder_id)
            previous_reminders = self.load_reminders(user_id)
            if reminder_id > 0 and reminder_id <= len(previous_reminders):
                x = reminder_id-1
                deleted_element = previous_reminders.pop(x)
                job_id = user_id+"-"+deleted_element["job_id"]
                job_instance = scheduler.get_job(job_id)
                if job_instance:
                    job_instance.remove()
                    save(user_id, previous_reminders)
                    return "Reminder Deleted"
                else:
                    return "Could not find background job"

            else:
                return "Nothing to forget"
        else:
            return "Nothing to forget"

    def clear_one_timers(self, user_id, reminder_id, scheduler):
        rid = reminder_id.replace(f"{user_id}-", '')
        previous_reminders = self.load_reminders(user_id)

        found_index = -1
        for ind, pr in enumerate(previous_reminders):
            if pr['job_id'] == rid:
                found_index = ind

        if found_index > -1:
            scheduler.remove_job(reminder_id)
            previous_reminders.pop(found_index)

        save(user_id, previous_reminders)
