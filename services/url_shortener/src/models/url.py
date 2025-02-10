from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.database.models.base import STR_10, STR_512, Base
from core.database.models.mixins import AccessedAtMixin, CreatedAtMixin, IdMixin, UpdatedAtMixin
from schemas.url import UrlVisibility


class Url(Base, IdMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "url"

    original_url: Mapped[STR_512] = mapped_column(nullable=False)
    short_id: Mapped[STR_10] = mapped_column(unique=True, index=True)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int | None] = mapped_column(nullable=True)
    visibility: Mapped[UrlVisibility] = mapped_column(default=False)


class UrlStats(Base, AccessedAtMixin):
    __tablename__ = "url_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    url_id: Mapped[int] = mapped_column(ForeignKey("url.id"))
    client_info: Mapped[STR_512] = mapped_column(nullable=True)
