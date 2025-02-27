from sqlalchemy import Column, Integer, BigInteger, ForeignKey, Boolean, String, ARRAY, TIMESTAMP
from sqlalchemy.orm import relationship

from .Base import Base
################################################################################

__all__ = ("ProfileAdditionalImageModel", "StaffProfileModel")

################################################################################
class ProfileAdditionalImageModel(Base):

    __tablename__ = "profile_additional_images"

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("staff_profiles.user_id", name="profile_additional_images_profile_fkey", ondelete="CASCADE"), nullable=False)
    url = Column(String, nullable=False)
    caption = Column(String, nullable=True)

    # Relationships
    profile = relationship("StaffProfileModel", back_populates="additional_images", passive_deletes=True)

################################################################################
class StaffProfileModel(Base):

    __tablename__ = "staff_profiles"

    top_level_id = Column(Integer, ForeignKey("top_level.id", name="bg_checks_top_level_fkey", ondelete="CASCADE"), nullable=False, server_default="1")
    # Main Data
    user_id = Column(BigInteger, primary_key=True)
    post_url = Column(String, nullable=True)
    # Details
    name = Column(String, nullable=True)
    url = Column(String, nullable=True)
    color = Column(Integer, nullable=True)
    jobs = Column(ARRAY(String), nullable=False, server_default="{}")
    rates = Column(String, nullable=True)
    position_ids = Column(ARRAY(Integer), nullable=False, server_default="{}")
    dm_pref = Column(Boolean, nullable=False, server_default="false")
    timezone = Column(Integer, nullable=False, server_default="7")
    # At A Glance
    gender = Column(String, nullable=True)
    pronouns = Column(ARRAY(Integer), nullable=False, server_default="{}")
    race = Column(String, nullable=True)
    clan = Column(String, nullable=True)
    orientation = Column(String, nullable=True)
    height = Column(Integer, nullable=True)
    age = Column(String, nullable=True)
    mare = Column(String, nullable=True)
    data_centers = Column(ARRAY(Integer), nullable=False, server_default="{}")
    # Personality
    likes = Column(ARRAY(String), nullable=False, server_default="{}")
    dislikes = Column(ARRAY(String), nullable=False, server_default="{}")
    personality = Column(String, nullable=True)
    about_me = Column(String, nullable=True)
    # Images
    thumbnail_url = Column(String, nullable=True)
    main_image_url = Column(String, nullable=True)

    # Relationships
    top_level = relationship("TopLevelDataModel", back_populates="profiles", passive_deletes=True)
    additional_images = relationship("ProfileAdditionalImageModel", back_populates="profile", passive_deletes=True)

################################################################################
