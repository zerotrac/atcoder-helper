from time import sleep

from requests_html import HTMLSession
from requests.exceptions import RequestException

class AtcoderTestcaseExtractor:
    def __init__(self):
        self.host_url = "https://atcoder.jp"
        self.tasks_page_url = self.host_url + "/contests/{}/tasks"

        self.session = HTMLSession()
    
    def safe_get(self, url):
        while True:
            try:
                response = self.session.get(url)
            except RequestException as e:
                sleep(5)
            else:
                return response

    def get_tasks_table(self, contest_id):
        """
        Get the html table element which contains all the tasks and links.
        """
        tasks_page = self.safe_get(self.tasks_page_url.format(contest_id))
        tasks_table = tasks_page.html.find(".table")

        # Make sure that there is only one table,
        # otherwise the structure of the page may have been modified.
        assert len(tasks_table) == 1

        return tasks_table[0]

    def get_tasks(self, contest_id):
        """
        Return a list of tasks which is in the form of (task_id, task_name, task_link) tuples
        """
        tasks_table = self.get_tasks_table(contest_id)
        task_lines = tasks_table.find("tbody tr")
        tasks = list()
        for task_line in task_lines:
            tds = task_line.find("td")
            tasks.append((tds[0].text, tds[1].text, self.host_url + tds[1].links.pop()))
        
        print(tasks)
        return tasks

    def execute(self, contest_id):
        tasks = self.get_tasks(contest_id)


if __name__ == "__main__":
    AtcoderTestcaseExtractor().execute("abc185")