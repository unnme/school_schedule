from app.core.logging_config import get_logger
from app.entities.classroom.repository import ClassroomRepository
from app.entities.student_group.repository import StudentGroupRepository
from app.entities.subject.repository import SubjectRepository
from app.entities.teacher.repository import TeacherRepository

logger = get_logger(__name__)

subject_repository = SubjectRepository()
student_group_repository = StudentGroupRepository()
teacher_repository = TeacherRepository()
classroom_repository  = ClassroomRepository()





