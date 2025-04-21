from random import choice, randint
from typing import List, Dict

from faker import Faker
from faker.providers import BaseProvider
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import session_manager
from backend.entities.classroom.schemas import ClassroomPostRequest
from backend.entities.subject.schemas import SubjectPostRequest
from backend.entities.teacher.schemas import TeacherPostRequest
from backend.entities.teacher.repository import teacher_repository
from backend.entities.classroom.repository import classroom_repository
from backend.entities.subject.repository import subject_repository


class RussianPatronymicProvider(BaseProvider):
    patronymics = [
        "Александров",
        "Алексеев",
        "Дмитриев",
        "Иванов",
        "Сергеев",
        "Павлов",
        "Владимиров",
        "Михайлов",
        "Олегов",
    ]

    def patronymic_male(self):
        return self.random_element(self.patronymics) + "ич"

    def patronymic_female(self):
        return self.random_element(self.patronymics) + "на"


class BaseFactory:
    fake = Faker("ru_RU")
    fake.add_provider(RussianPatronymicProvider)

    @classmethod
    def _rand_hours(cls):
        return randint(10, 60)


class ClassroomFactory(BaseFactory):
    letters = ["а", "б", "в"]

    @classmethod
    def generate_names(cls) -> List[str]:
        names = []
        for num in range(1, 20):
            for i in range(randint(1, len(cls.letters))):
                names.append(f"{num}-{cls.letters[i]}")
        return names

    @classmethod
    def make_requests(cls, names: List[str]) -> List[ClassroomPostRequest]:
        return [ClassroomPostRequest(name=n) for n in names]


class SubjectFactory(BaseFactory):
    SUBJECT_NAMES = [
        "Математика",
        "Физика",
        "Химия",
        "Биология",
        "История",
        "Литература",
        "География",
        "Информатика",
        "Английский язык",
        "Обществознание",
    ]

    @classmethod
    def make_requests(cls) -> List[SubjectPostRequest]:
        return [SubjectPostRequest(name=name) for name in cls.SUBJECT_NAMES]

    @classmethod
    def get_subject_count(cls) -> int:
        return len(cls.SUBJECT_NAMES)


class TeacherFactory(BaseFactory):
    @classmethod
    def _generate_names(cls, count: int) -> List[Dict]:
        names, seen = [], set()
        while len(names) < count:
            is_male = choice([True, False])
            first = (
                cls.fake.first_name_male() if is_male else cls.fake.first_name_female()
            )
            last = cls.fake.last_name_male() if is_male else cls.fake.last_name_female()
            patronymic = (
                cls.fake.patronymic_male() if is_male else cls.fake.patronymic_female()
            )
            full = f"{first} {last} {patronymic}"
            if full not in seen:
                seen.add(full)
                names.append(
                    {"first_name": first, "last_name": last, "patronymic": patronymic}
                )
        return names

    @classmethod
    def _generate_subjects(cls) -> List[Dict]:
        ids = set()
        subject_count = SubjectFactory.get_subject_count()
        while len(ids) < randint(1, 3):
            ids.add(randint(1, subject_count))
        return [{"id": sid, "teaching_hours": cls._rand_hours()} for sid in ids]

    @classmethod
    def make_requests(cls, count: int) -> List[TeacherPostRequest]:
        people = cls._generate_names(count)
        return [
            TeacherPostRequest(**person, subjects=cls._generate_subjects())  # pyright: ignore
            for person in people
        ]


class Seeder:
    TEACHER_COUNT = 10

    @classmethod
    async def seed_all(cls):
        async for session in session_manager.get_async_session():
            await cls._seed_classrooms(session)
            await cls._seed_subjects(session)
            await cls._seed_teachers(session)

    @classmethod
    async def _seed_classrooms(cls, session: AsyncSession):
        names = ClassroomFactory.generate_names()
        data = ClassroomFactory.make_requests(names)
        await classroom_repository.create_many(session, data)

    @classmethod
    async def _seed_subjects(cls, session: AsyncSession):
        data = SubjectFactory.make_requests()
        await subject_repository.create_many(session, data)

    @classmethod
    async def _seed_teachers(cls, session: AsyncSession):
        data = TeacherFactory.make_requests(cls.TEACHER_COUNT)
        await teacher_repository.create_many(session, data)
