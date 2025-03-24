from random import choice, randint
from typing import Dict, List

from faker import Faker
from faker.providers import BaseProvider
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.depends.repository import teacher_repository
from backend.core.database import session_manager
from backend.core.managers import EntitiesInitManager
from backend.entities.teacher.schemas import TeacherCreateRequest

TEACHERS_COUNT = 10
fake = Faker("ru_RU")


class RussianPatronymicProvider(BaseProvider):
    patronymics = [
        f"Александров",
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
        return str(self.random_element(self.patronymics) + "ич")

    def patronymic_female(self):
        return str(self.random_element(self.patronymics) + "на")


fake.add_provider(RussianPatronymicProvider)


class F:
    classroom_names = [
        "1",
        "1-а",
        "1-б",
        "2",
        "2-а",
        "2-б",
        "3",
        "3-а",
        "3-б",
        "4",
        "4-а",
        "4-б",
        "5",
        "5-а",
        "5-б",
        "6",
        "6-а",
        "6-б",
        "7",
        "7-а",
        "7-б",
        "8",
        "8-а",
        "8-б",
        "9",
        "9-а",
        "9-б",
        "10",
        "10-а",
        "10-б",
        "11",
        "11-а",
        "11-б",
        "12",
        "12-а",
        "12-б",
        "13",
        "13-а",
        "13-б",
        "14",
        "14-а",
        "14-б",
        "15",
        "15-а",
        "15-б",
        "16",
        "16-а",
        "16-б",
        "17",
        "17-а",
        "17-б",
        "18",
        "18-а",
        "18-б",
        "19",
        "19-а",
        "19-б",
        "20",
        "20-а",
        "20-б",
    ]

    subject_names = [
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
    def _rand_subject_id(cls):
        return randint(1, len(cls.subject_names))

    @classmethod
    def _rand_hours(cls):
        return randint(10, 60)

    @classmethod
    def _get_teacher_names(cls, count: int) -> List:
        full_name_list = []
        full_name_set = set()
        while len(full_name_list) < count:
            is_male = choice([True, False])
            first_name = fake.first_name_male() if is_male else fake.first_name_female()
            last_name = fake.last_name_male() if is_male else fake.last_name_female()
            patronymic = fake.patronymic_male() if is_male else fake.patronymic_female()

            full_name = f"{first_name} {last_name} {patronymic}"

            if full_name not in full_name_set:
                full_name_set.add(full_name)
                full_name_list.append(
                    {
                        "first_name": first_name,
                        "last_name": last_name,
                        "patronymic": patronymic,
                    }
                )

        return full_name_list

    @classmethod
    def _make_teacher_subjects(cls):
        _list = []
        _set = set()
        target_size = randint(1, 3)
        while len(_list) < target_size:
            id = cls._rand_subject_id()
            if id not in _set:
                _set.add(id)
                _list.append({"id": id, "teaching_hours": cls._rand_hours()})

        return _list

    @classmethod
    async def fake_teachers(cls, session: AsyncSession, count: int):
        teacher_names: List[Dict] = cls._get_teacher_names(count)
        request_data_list = [
            TeacherCreateRequest(
                first_name=full_name["first_name"],
                last_name=full_name["last_name"],
                patronymic=full_name["patronymic"],
                subjects=cls._make_teacher_subjects(),
            )
            for full_name in teacher_names
        ]
        await teacher_repository.create_many(session, request_data_list)

    # @classmethod
    # async def fake_student_groups(cls, count: int):
    #     async for session in sm.get_async_session():
    #         StudentGroupCreateRequest(
    #             name="",
    #             capacity=33,
    #             subjects=[]
    #         )

    @classmethod
    async def fake_lessons(cls, session: AsyncSession):
        pass

    @classmethod
    async def generate_fake_data(cls):
        async for session in session_manager.get_async_session():
            await EntitiesInitManager.init_classrooms(session, cls.classroom_names)
            await EntitiesInitManager.init_subjects(session, cls.subject_names)

            await cls.fake_teachers(session, count=TEACHERS_COUNT)
            # await cls.fake_student_groups(session)
            # await cls.fake_lessons(session)
