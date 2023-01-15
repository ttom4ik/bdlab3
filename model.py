from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, select, and_, DATETIME, exc
from sqlalchemy.orm import relationship
from config import Session, engine, base

ses = Session()
connection = None


class Direction(base):
    __tablename__ = 'Direction'
    number = Column(Integer, primary_key=True, nullable=False)
    number_med = Column(Integer, ForeignKey('Patient.number_med'), nullable=False)
    id_doctor = Column(Integer, ForeignKey('Doctor.id_doctor'), nullable=False)
    id_specialist = Column(Integer, ForeignKey('Specialist.id_specialist'), nullable=False)
    data = Column(String(50), nullable=False)
    Doctor = relationship('Doctor')
    Specialist = relationship('Specialist')
    Patient = relationship('Patient')

    def __init__(self, number_med, id_doctor, id_specialist, data, number=-1):
        self.number_med = number_med
        self.id_doctor = id_doctor
        self.id_specialist = id_specialist
        self.data = data
        if id != -1:
            self.number = number

    format_str = '{:^8}{:^12}{:^12}{:^12}{:^20}'

    def __repr__(self):
        return self.format_str.format(self.number, self.number_med, self.id_doctor, self.id_specialist, self.data)

    def __attributes_print__(self):
        return self.format_str.format('number', 'number_med', 'id_doctor', 'id_specialist', 'data')


class Doctor(base):
    __tablename__ = 'Doctor'
    id_doctor = Column(Integer, primary_key=True, nullable=False)
    id_specialist = Column(Integer, ForeignKey('Specialist.id_specialist'), nullable=False)
    name_doc = Column(String(50), nullable=False)
    phone_num = Column(Integer, nullable=False)
    Specialist = relationship('Specialist')

    def __init__(self, id_specialist, name_doc, phone_num, id_doctor=-1):
        self.phone_num = phone_num
        self.id_specialist = id_specialist
        self.name_doc = name_doc
        if id_doctor != -1:
            self.id_doctor = id_doctor

    format_str = '{:^10}{:^12}{:^12}{:^30}'

    def __repr__(self):
        return self.format_str.format(self.id_doctor, self.id_specialist, self.name_doc, self.phone_num)

    def __attributes_print__(self):
        return self.format_str.format('id_doctor', 'id_specialist', 'name_doc', 'phone_num')


class Hospital(base):
    __tablename__ = 'Hospital'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    phone = Column(Integer, nullable=False)

    def __init__(self, name, address, phone, id=-1):
        self.phone = phone
        self.name = name
        self.address = address
        if id != -1:
            self.id = id

    format_str = '{:^8}{:^30}{:^40}{:^20}'

    def __repr__(self):
        return self.format_str.format(self.id, self.name, self.address, self.phone)

    def __attributes_print__(self):
        return self.format_str.format('id', 'name', 'address', 'phone')


class Hospital_Doctor(base):
    __tablename__ = 'Hospital_Doctor'
    id_tab = Column(Integer, primary_key=True, nullable=False)
    id = Column(Integer, ForeignKey('Hospital.id'), nullable=False)
    id_doctor = Column(Integer, ForeignKey('Doctor.id_doctor'), nullable=False)
    Hospital = relationship('Hospital')
    Doctor = relationship('Doctor')

    def __init__(self, id, id_doctor, id_tab=-1):
        self.id_doctor = id_doctor
        self.id = id
        if id_tab != -1:
            self.id_tab = id_tab

    format_str = '{:^8}{:^12}{:^12}'

    def __repr__(self):
        return self.format_str.format(self.id_tab, self.id, self.id_doctor)

    def __attributes_print__(self):
        return self.format_str.format('id_tab', 'id', 'id_doctor')


class Patient(base):
    __tablename__ = 'Patient'
    number_med = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)

    def __init__(self, name, number_med=-1):
        self.name = name
        if number_med != -1:
            self.number_med = number_med

    format_str = '{:^10}{:^30}'

    def __repr__(self):
        return self.format_str.format(self.number_med, self.name)

    def __attributes_print__(self):
        return self.format_str.format('number_med', 'name')


class Specialist(base):
    __tablename__ = 'Specialist'
    id_specialist = Column(Integer, primary_key=True, nullable=False)
    cabinet = Column(Integer, nullable=False)
    specialization = Column(String(50), nullable=False)

    def __init__(self, cabinet, specialization, phone, id_specialist=-1):
        self.phone = phone
        self.name = name
        self.specialization = specialization
        if id_specialist != -1:
            self.id_specialist = id_specialist

    format_str = '{:^12}{:^12}{:^40}'

    def __repr__(self):
        return self.format_str.format(self.id_specialist, self.cabinet, self.specialization)

    def __attributes_print__(self):
        return self.format_str.format('id_specialist', 'cabinet', 'specialization')


def connect():
    # global connection = engine.connect()
    base.metadata.create_all(engine)


def insert(num: int, col: list) -> bool:
    if len(col) < 1:
        return false
    element = None
    try:
        match num:
            case 1:
                element = Direction(*col)
            case 2:
                element = Doctor(*col)
            case 3:
                element = Hospital(*col)
            case 4:
                element = Hospital_Doctor(*col)
            case 5:
                element = Patient(*col)
            case 6:
                element = Specialist(*col)
        ses.add(element)
        ses.commit()
    except (Exception, exc.DBAPIError) as error:
        print("Can't insert into table", error)
        ses.rollback()
        return False
    return True


def myselect(num: int, quantity: int = 100, offset: int = 0, id: str = "") -> list:
    table = None
    primary_key = None
    if id:
        id = int(id)
    try:
        match num:
            case 1:
                if id:
                    return ses.query(Direction).filter_by(number=id).limit(quantity).all()
                else:
                    return ses.query(Direction).order_by(Direction.number.asc()).offset(offset).limit(quantity).all()
            case 2:
                if id:
                    return ses.query(Doctor).filter_by(id_doctor=id).limit(quantity).all()
                else:
                    return ses.query(Doctor).order_by(Doctor.id_doctor.asc()).offset(offset).limit(quantity).all()
            case 3:
                if id:
                    return ses.query(Hospital).filter_by(id=id).limit(quantity).all()
                else:
                    return ses.query(Hospital).order_by(Hospital.id.asc()).offset(offset).limit(quantity).all()
            case 4:
                if id:
                    return ses.query(Hospital_Doctor).filter_by(id_tab=id).limit(quantity).all()
                else:
                    return ses.query(Hospital_Doctor).order_by(Hospital_Doctor.id_tab.asc()).offset(offset).limit(
                        quantity).all()
            case 5:
                if id:
                    return ses.query(Patient).filter_by(number_med=id).limit(quantity).all()
                else:
                    return ses.query(Patient).order_by(Patient.number_med.asc()).offset(offset).limit(quantity).all()
            case 6:
                if id:
                    return ses.query(Specialist).filter_by(id_specialist=id).limit(quantity).all()
                else:
                    return ses.query(Specialist).order_by(Specialist.id_specialist.asc()).offset(offset).limit(
                        quantity).all()

    except (Exception, exc.DBAPIError) as error:
        print("Can't select table", error)
        ses.rollback()
        return []


def delete(num: int, id: str) -> bool:
    try:
        match num:
            case 1:
                ses.query(Direction).filter_by(number=int(id)).delete()
            case 2:
                ses.query(Doctor).filter_by(id_doctor=id).delete()
            case 3:
                ses.query(Hospital).filter_by(id=id).delete()
            case 4:
                ses.query(Hospital_Doctor).filter_by(id_tab=int(id)).delete()
            case 5:
                ses.query(Specialist).filter_by(number_med=int(id)).delete()
            case 6:
                ses.query(Specialist).filter_by(id_specialist=int(id)).delete()
        ses.commit()
    except (Exception, exc.DBAPIError) as error:
        print("Can't delete from table", error)
        ses.rollback()
        return False
    return True


def update(num: int, col: list, id: str) -> bool:
    try:
        match num:
            case 1:
                ses.query(Direction).filter_by(number=int(id)).update(
                    {Direction.number_med: col[0], Direction.id_doctor: col[1], Direction.id_specialist: col[2],
                     Direction.data: col[2]})
            case 2:
                ses.query(Doctor).filter_by(id_doctor=id).update(
                    {Doctor.id_specialist: col[0], Doctor.name_doc: col[1], Doctor.phone_num: col[2]})
            case 3:
                ses.query(Hospital).filter_by(id=id).update(
                    {Hospital.name: col[0], Hospital.address: col[1], Hospital.phone: col[2]})
            case 4:
                ses.query(Hospital_Doctor).filter_by(id_tab=int(id)).update(
                    {Hospital_Doctor.id: col[0], Hospital_Doctor.id_doctor: col[1]})
            case 5:
                ses.query(Patient).filter_by(number_med=int(id)).update(
                    {Patient.name: col[0]})
            case 6:
                ses.query(Specialist).filter_by(id_specialist=int(id)).update(
                    {Specialist.cabinet: col[0], Specialist.specialization: col[1]})
        ses.commit()
    except (Exception, exc.DBAPIError) as error:
        print("Can't update table", error)
        ses.rollback()
        return False
    return True