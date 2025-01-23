from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.models.examen import ExamenModel
from app.schemas.examenes import ExamenSchema

class ExamenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_examen(self, examen_data: ExamenSchema, user_uid: str, username: str):
        # Crear un nuevo examen en la base de datos
        examen = ExamenModel(
            user_uid=user_uid,
            user_name=username,
            exam_type=examen_data.exam_type,
            res_1=examen_data.res_1,
            res_2=examen_data.res_2,
            res_3=examen_data.res_3,
            res_4=examen_data.res_4,
            res_5=examen_data.res_5,
            res_6=examen_data.res_6,
            res_7=examen_data.res_7,
            res_8=examen_data.res_8,
            res_9=examen_data.res_9,
            res_10=examen_data.res_10,
            total_percentage=examen_data.total_percentage,
        )
        self.db.add(examen)
        await self.db.commit()
        await self.db.refresh(examen)
        return examen

    async def get_all_examenes(self):
        # Obtener todos los exámenes
        query = select(ExamenModel)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_examenes_by_user_uid(self, user_uid: str):
        # Obtener los exámenes de un usuario específico
        query = select(ExamenModel).where(ExamenModel.user_uid == user_uid)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_examen_by_id(self, examen_id: int):
        # Obtener un examen por su ID
        query = select(ExamenModel).where(ExamenModel.id_examen == examen_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def delete_examen(self, examen_id: int):
        # Eliminar un examen
        query = delete(ExamenModel).where(ExamenModel.id_examen == examen_id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount  # Devuelve cuántos registros fueron eliminados

    async def update_examen(self, examen_id: int, examen_data: ExamenSchema):
        # Actualizar un examen
        query = (
            update(ExamenModel)
            .where(ExamenModel.id_examen == examen_id)
            .values(
                exam_type=examen_data.exam_type,
                res_1=examen_data.res_1,
                res_2=examen_data.res_2,
                res_3=examen_data.res_3,
                res_4=examen_data.res_4,
                res_5=examen_data.res_5,
                res_6=examen_data.res_6,
                res_7=examen_data.res_7,
                res_8=examen_data.res_8,
                res_9=examen_data.res_9,
                res_10=examen_data.res_10,
                total_percentage=examen_data.total_percentage,
            )
        )
        await self.db.execute(query)
        await self.db.commit()
        # Recuperar el examen actualizado
        return await self.get_examen_by_id(examen_id)
