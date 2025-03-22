from backend.api.depends.repository import classroom_repository
from backend.core.database import session_manager as smngr
from backend.core.logging_config import get_logger
from backend.entities.classroom.schemas import ClassroomCreateRequest
from backend.utils.db_utils import DatabaseManager
from tests.main import F

logger = get_logger(__name__)


class ClassroomService:
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

    @classmethod
    async def init_classrooms(cls):
        async for session in smngr.get_async_session():
            request_data_list = [
                ClassroomCreateRequest(name=name) for name in cls.classroom_names
            ]

            await classroom_repository.create_many(session, request_data_list)


async def first_run() -> None:
    # await DatabaseManager._drop_all_tables()  # WARN: REMOVE THIS!

    if not await DatabaseManager.check_db_tables():
        logger.info("🌟 Starting first run setup...")

        await DatabaseManager.create_db_tables()

        logger.info("✅ First run setup completed.")

        await ClassroomService.init_classrooms()

        await F.generate_fake_data()
