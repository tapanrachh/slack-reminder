from helper import remove_extra_spaces
from Reminder import Reminder
reminder = Reminder()


def slack_parser(s, channel_id, foo, scheduler):
    s = remove_extra_spaces(s)

    out_msg = "Please Type\n1 to get all options\n2 to set daily reminder\n3 to get all reminders\n4 to forget a reminder"
    if s == "1":
        pass
    if s == "2":
        out_msg = "To set reminder type\nremind [text to remind] at [0-23]:[0:59]:[0:59] eg. remind update log sheet 19:25 (add -o to get reminded only once) "
    if s == "3":
        out_msg = reminder.get_reminders(channel_id)
    if s == "4":
        out_msg = "To delete reminder type\nforget [reminderId]"
    if s.startswith("remind"):
        s = s.replace('remind', '', 1)
        at_index = s.rfind("at")
        content = s[:at_index]

        if "-o" in s:
            daily = False
            s = s.replace("-o", "")
        else:
            daily = True

        time = s[at_index+2:]

        content = remove_extra_spaces(content)
        time = remove_extra_spaces(time)
        time = time.split(":")
        hh = time[0]
        mm = time[1]

        out_msg = reminder.add_reminder(
            channel_id, content, hh, mm, foo, scheduler, daily)
    if s.startswith("forget"):
        s = s.replace('forget', '', 1)
        s = remove_extra_spaces(s)
        out_msg = reminder.delete_reminder(channel_id, s, scheduler)

    return out_msg
