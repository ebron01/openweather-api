from sqlalchemy.orm import Session

from . import models, schemas


def get_city(db: Session, city: str):
    if db.query(models.City).filter(models.City.name == city).first():
        return db.query(models.City).filter(models.City.name == city).first()
    return None


def get_cities(db: Session, skip: int = 0, limit: int = 0):
    return db.query(models.City).offset(skip).limit(limit).all()


def create_report(db: Session, report: schemas.Report):
    db_report = models.Report(**report.dict())
    db.add(db_report)
    db.commit()
    # db.refresh()
    return db_report


def create_city(db: Session, city: schemas.City):
    db_city = models.City(**city.dict())
    db.add(db_city)
    db.commit()
    # db.refresh()
    return db_city

def get_reports(db : Session, city: schemas.City):
    return db.query(models.Report).filter(models.Report.name == city)


def create_report_bulk(db: Session, reports: schemas.ReportBulk):
    for report in reports:
        db_report = models.ReportBulk(**report)
        db.add(db_report)
    db.commit()
    # db.refresh()
    return reports
