import markdown

import sqlite3


class Database:

    def __init__(self, path):
        self.conn = sqlite3.connect(path)

    def select(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        return c.fetchall()

    def execute(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        self.conn.commit()
    
    def get_last_modification_info(self, article_id):
        data = self.select(
            'SELECT MAX(submission_time), username FROM contributor WHERE article_id = ? GROUP BY username', [article_id])
        return {'last_modification_time': data[0][0], 'last_modifier_username': data[0][1]}
    
    def get_contributor_info(self, article_id):
        data = self.select(
            'SELECT * FROM contributor WHERE article_id = ? ORDER BY submission_time ASC', [article_id])
        return [{
            'modification_time': d[1],
            'modifying_username': d[3],
        } for d in data]
    
    def get_article(self, article_id):
        data = self.select(
            'SELECT * FROM article WHERE id = ?', [article_id])[0]
        return {
            'id': data[0],
            'title': data[1],
            'content': markdown.markdown(data[2]),
            'votes': data[3],
        }
    
    def get_raw(self, article_id):
        data = self.select(
            'SELECT title, content FROM article WHERE id = ?', [article_id])[0]
        return {'title': data[0], 'content': data[1]}
    
    def get_num_articles(self):
        data = self.select(
            'SELECT COUNT(*) FROM article')[0]
        return data[0]
    
    def get_articles_by(self, username):
        data = self.select(
            'SELECT DISTINCT article_id FROM contributor WHERE username = ?', [username])
        return [self.get_article(article_id[0]) for article_id in data]
    
    def get_rep(self, username):
        import random
        return random.choice([38, 56, 27])
    
    def get_recent(self):
        data = self.select(
            'SELECT DISTINCT article_id FROM contributor ORDER BY submission_time desc LIMIT 30')
        return [{
            **self.get_article(article_id[0]),
            **self.get_last_modification_info(article_id[0]),
        } for article_id in data]
    
    def apply_vote(self, article_id, delta):
        self.execute(
            f'UPDATE article SET votes = votes + {delta} WHERE id = ?', [article_id])
    
    def create_user(self, username, encrypted_password):
        self.execute('INSERT INTO user (username, encrypted_password) VALUES (?, ?)',
                     [username, encrypted_password])

    def get_user(self, username):
        data = self.select(
            'SELECT * FROM user WHERE username=?', [username])
        if data:
            d = data[0]
            return {
                'username': d[0],
                # 'email': d[1],
                'encrypted_password': d[1],
                'reputation': d[2],
            }
        else:
            return None

    def close(self):
        self.conn.close()
