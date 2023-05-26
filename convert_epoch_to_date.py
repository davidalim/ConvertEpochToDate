import sublime
import sublime_plugin
import re
from datetime import datetime

def getSettings(string):
    return sublime.load_settings('ConvertEpochToDate.sublime-settings').get(string)

class ConvertEpochToDateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view; msg = ''
        for region in view.sel():
            if region.empty():
                region = view.word(region)

            epoch_text = view.substr(region)
            if epoch_text and re.match(r'^(\d{10,13})$', epoch_text):

                output_date_format = getSettings('output_date_format')
                try:
                    result = datetime.fromtimestamp(int(epoch_text[0:10])).strftime(output_date_format)
                except ValueError:
                    msg = ' (Warning: Invalid format string \'' + output_date_format + '\' defined, using default)'
                    output_date_format = '%a %d %b %Y %I:%M:%S %p'
                    result = datetime.fromtimestamp(int(epoch_text[0:10])).strftime(output_date_format)

                if result:
                    show_ms = getSettings('show_milliseconds')
                    if show_ms:
                        milsec = epoch_text[10:13]
                        if not milsec:
                            milsec = '0'
                        milsec = milsec.ljust(3, '0')
                        result = result + ' + ' + milsec + 'ms'

                    if view.is_read_only():
                        msg = ' (Warning: View readonly. Can\'t make inline replacement)'
                    else:
                        view.replace(edit, region, result)

                    msg = 'ConvertEpochToDate: ' + result + msg
                else:
                    msg = 'ConvertEpochToDate: Conversion error'
            else:
                msg = 'ConvertEpochToDate: Invalid epoch timestamp: \'' + epoch_text + '\'. Must be 10-13 digits'

            sublime.status_message(msg)
