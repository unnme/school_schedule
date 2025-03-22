from backend.core.logging_config import get_logger
from backend.entities.classroom.repository import ClassroomRepository
from backend.entities.lesson.repository import LessonRepository
from backend.entities.student_group.repository import StudentGroupRepository
from backend.entities.subject.repository import SubjectRepository
from backend.entities.teacher.repository import TeacherRepository

logger = get_logger(__name__)

subject_repository = SubjectRepository()
student_group_repository = StudentGroupRepository()
teacher_repository = TeacherRepository()
classroom_repository = ClassroomRepository()
lesson_repository = LessonRepository()
