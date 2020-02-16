import unittest

from mongoengine import connect, Document, StringField, FileField

connect(db='rtz_2', host='192.168.0.105', port=27017,
        username='root',
        password='123456',
        authentication_source='admin')


class RtzDoc(Document):
    suffix = StringField()
    url = StringField()
    photo = FileField()


class MyTestCase(unittest.TestCase):
    def test_something(self):
        # 从mongo中取出图片
        rtz_doc = RtzDoc.objects().get(id='5e3e4d641ea3649bc2eb86aa')
        photo = rtz_doc.photo
        with open('/home/john/tmp/images/'+ str(rtz_doc.id) + rtz_doc.suffix, 'wb') as f:
            f.write(photo.read())

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
