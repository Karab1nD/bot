import datetime
import json


class Task:
    def __init__(self, title, note):
        self.date = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
        self.title = title
        self.note = note


class TaskOrganizer:
    def __init__(self):
        self.tasks = []

    def save_to_file(self, fileId, task):
        data_from_file = self.load_from_file(fileId)

        task_data = []

        if data_from_file:
            for data in data_from_file:
                data_dict = {
                    'date': data.date,
                    'title': data.title,
                    'note': data.note
                }
                task_data.append(data_dict)

        task_dict = {
            'date': task.date,
            'title': task.title,
            'note': task.note
        }
        task_data.append(task_dict)

        with open(f'tasks{fileId}.json', 'w') as file:
            json.dump(task_data, file, indent=4, ensure_ascii=True)

    def load_from_file(self, fileID):
        try:
            with open(f'tasks{fileID}.json', 'r') as f:
                content = f.read()
                if not content:
                    print('file is empty')
                    return []

                tasks_data = json.loads(content)
                out_data = []

                if tasks_data:
                    for data in tasks_data:
                        task = Task(data['title'], data['note'])
                        task.date = data['date']
                        out_data.append(task)
                    return out_data
                else:
                    return out_data

        except FileNotFoundError:
            print('File not found')
            return []
        except json.JSONDecodeError:
            print('json is bad')
            return []

    def add_task(self, fileId, title, note):
        task = Task(title, note)
        # self.tasks.append(task)
        self.save_to_file(fileId, task)

    def view_tasks(self, fileID):
        out_data = self.load_from_file(fileID)
        return out_data

    def del_task(self, fileId, num_task):
        data_file = self.load_from_file(fileId)
        if data_file:
            if 1 <= num_task <= len(data_file):
                task = data_file[num_task - 1]
                data_file.remove(task)
                # распаковать объект перед записью в JSON
                data_to_json = []
                for data in data_file:
                    data_dict = {
                        'date': data.date,
                        'title': data.title,
                        'note': data.note
                    }
                    data_to_json.append(data_dict)

                with open(f'tasks{fileId}.json', 'w') as file:
                    json.dump(data_to_json, file, indent=4, ensure_ascii=True)

    def edit_title(self, fileId, num_task, new_title):
        data_file = self.load_from_file(fileId)
        if data_file:
            if 1 <= num_task <= len(data_file):
                # распаковать объект перед записью в JSON
                data_to_json = []
                n = 1
                for data in data_file:
                    if n == num_task:
                        title = new_title
                    else:
                        title = data.title
                    data_dict = {
                        'date': data.date,
                        'title': title,
                        'note': data.note
                    }
                    data_to_json.append(data_dict)
                    n += 1

                with open(f'tasks{fileId}.json', 'w') as file:
                    json.dump(data_to_json, file, indent=4, ensure_ascii=True)

    def edit_note(self, fileId, num_task, new_note):
        data_file = self.load_from_file(fileId)
        if data_file:
            if 1 <= num_task <= len(data_file):
                # распаковать объект перед записью в JSON
                data_to_json = []
                n = 1
                for data in data_file:
                    if n == num_task:
                        note = new_note
                    else:
                        note = data.title
                    data_dict = {
                        'date': data.date,
                        'title': data.title,
                        'note': note
                    }
                    data_to_json.append(data_dict)
                    n += 1

                with open(f'tasks{fileId}.json', 'w') as file:
                    json.dump(data_to_json, file, indent=4, ensure_ascii=True)

    def edit_code(self, fileId, num_task, new_code):
        data_file = self.load_from_file(fileId)
        if data_file:
            if 1 <= num_task <= len(data_file):
                # распаковать объект перед записью в JSON
                data_to_json = []
                n = 1
                for data in data_file:
                    if n == num_task:
                        code = new_code
                    else:
                        code = data.title
                    data_dict = {
                        'date': data.date,
                        'title': data.title,
                        'note': data.note
                    }
                    data_to_json.append(data_dict)
                    n += 1

                with open(f'tasks{fileId}.json', 'w') as file:
                    json.dump(data_to_json, file, indent=4, ensure_ascii=True)

    def save_user_data(self, userid, username, x):
        users = []
        try:
            with open('users.txt') as file:
                for line in file:
                    users.append(line.strip().split(':')[0])
            if str(userid) in users:
                return
        except FileNotFoundError:
            pass

        with open('users.txt', 'a') as file:
            file.write(f'{userid}:{username}:{x}\n')

    def read_users(self):
        users = []
        try:
            with open('users.txt') as file:
                for line in file:
                    userid, username = line.strip().split(':')
                    users.append((userid, username))
            return users

        except FileNotFoundError:
            pass
