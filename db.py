import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, tg_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`tg_id`) VALUES (?)",
                                       (tg_id,))

    def user_exists(self, tg_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `tg_id` = ?",
                                         (tg_id,)).fetchall()
            return bool(len(result))

    def set_nickname(self, tg_id, tg_name):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `name` = ? WHERE `tg_id` = ?",
                                       (tg_name, tg_id,))

    def get_nickname(self, tg_id):
        with self.connection:
            result = self.cursor.execute("SELECT `name` FROM `users` WHERE `tg_id` = ?",
                                         (tg_id,)).fetchall()
            for row in result:
                nickname = str(row[0])
            return nickname

    def set_ans(self, ans, tg_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `ans` = ? WHERE `tg_id` = ?",
                                       (ans, tg_id,))

    def get_ans(self, tg_id):
        with self.connection:
            result = self.cursor.execute("SELECT `ans` FROM `users` WHERE `tg_id` = ?",
                                         [tg_id]).fetchall()
            return result[0][0]

    def get_info(self):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `info`").fetchall()

        ans = []
        for row in result:
            ans.append(row[1])
        return ans

    def get_ques(self):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `que`").fetchall()

            ans = []
            for row in result:
                ans.append({row[0]: {row[1]: row[2]}})
            return ans

    def set_tb(self, tb, tg_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `tb` = ? WHERE `tg_id` = ?",
                                       (tb, tg_id,))

    def get_tb(self, tg_id):
        with self.connection:
            result = self.cursor.execute("SELECT `tb` FROM `users` WHERE `tg_id` = ?",
                                         [tg_id]).fetchall()
            return result[0][0]
