class CommitRefreshMixin:
    @staticmethod
    async def commit_refresh(session, obj):
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj
