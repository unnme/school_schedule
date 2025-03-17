from src.core.logging_config import get_logger
from src.entities.classroom.repository import ClassroomRepository
from src.entities.student_group.repository import StudentGroupRepository
from src.entities.subject.repository import SubjectRepository
from src.entities.teacher.repository import TeacherRepository

logger = get_logger(__name__)

subject_repository = SubjectRepository()
student_group_repository = StudentGroupRepository()
teacher_repository = TeacherRepository()
classroom_repository = ClassroomRepository()
