from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage

_ltm_storage = LTMSQLiteStorage(db_path="shared/ltm.db")
_stm_storage = RAGStorage(type="short_term", path="shared/")
_entity_storage = RAGStorage(type="entities", path="shared/")

long_term_memory = LongTermMemory(storage=_ltm_storage)
short_term_memory = ShortTermMemory(storage=_stm_storage)
entity_memory = EntityMemory(storage=_entity_storage)