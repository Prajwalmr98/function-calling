from sqlalchemy import Integer, String, ForeignKey, create_engine, Column, Sequence, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class Employee(Base):
    __tablename__ = "emp"
    eid = Column("eid", Integer, primary_key=True)
    ename = Column("ename", String)
    esal = Column("esal", Integer)
    dnum = Column(Integer, ForeignKey("dept.deptno"))

    def __init__(self, eid, ename, esal, dnum):
        self.eid = eid
        self.ename = ename
        self.esal = esal
        self.dnum = dnum

    def __repr__(self):
        return f"({self.eid}) {self.ename} {self.dnum}"

class Department(Base):
    __tablename__ = "dept"
    loc = Column("loc", String, nullable=False)
    dname = Column("dname", String)
    deptno = Column(Integer, primary_key=True)

    def __init__(self, loc, dname, deptno):
        self.loc = loc
        self.dname = dname
        self.deptno = deptno

    def __repr__(self):
        return f"({self.loc}) {self.dname} owned by {self.deptno}"

# Use autoincrement for deptno or specify a sequence if necessary
engine = create_engine("sqlite:///db3.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

try:
    e1 = Employee(1, "virat", 100, 10)
    e2 = Employee(2, "rohit", 90, 20)
    e3 = Employee(3, "jadeja", 80, 30)
    e4 = Employee(4, "surya", 50, 40)

    d1 = Department("banglore", "batsman", 10)
    d2 = Department("mumbai", "captain", 20)
    d3 = Department("chennai", "spinner", 30)
    d4 = Department("Delhi", "alrounder", 50)

    session.add_all([e1, e2, e3, e4, d1, d2, d3,d4])
    session.commit()
except IntegrityError as e:
    session.rollback()
    print(f"An integrity error occurred: {e}")
except Exception as e:
    session.rollback()
    print(f"An error occurred: {e}")
finally:
    session.close()

# Perform queries
session = Session()

# Select employee and department details for employee with eid = 1
result = session.query(Employee, Department).filter(Employee.dnum == Department.deptno).filter(Employee.eid == 1).all()
for r in result:
    print(r)

# Update employee salary
update = session.query(Employee).filter(Employee.eid == 1).first()
if update:
    update.esal = 150
    session.commit()

# Calculate max, min, avg, sum, and count of salaries
maximum = session.query(func.max(Employee.esal)).scalar()
print(f"Max salary is: {maximum}")
minimum = session.query(func.min(Employee.esal)).scalar()
print(f"Min salary is: {minimum}")
avg = session.query(func.avg(Employee.esal)).scalar()
print(f"Avg salary is: {avg}")
sum_salary = session.query(func.sum(Employee.esal)).scalar()
print(f"Total salary is: {sum_salary}")
count = session.query(func.count(Employee.eid)).scalar()
print(f"Total number of employees is: {count}")

# Delete employee by name
def delete_employee_by_ename(ename):
    session = Session()
    try:
        employee_to_delete = session.query(Employee).filter(Employee.ename == ename).first()
        if employee_to_delete:
            session.delete(employee_to_delete)
            session.commit()
            print(f"Deleted employee with name: {ename}")
        else:
            print(f"No employee found with name: {ename}")
    except Exception as e:
        session.rollback()
        print(f"An error occurred while deleting employee: {e}")
    finally:
        session.close()

#delete_employee_by_ename("surya")

# Display all employees
display_all = session.query(Employee).all()
for emp in display_all:
    print(emp)

# Join employees with departments
join = session.query(Employee.ename, Department.loc).join(Department, Employee.dnum == Department.deptno).all()
for output in join:
    print(output)

session.close()
#left outerjoin
leftouter_join=session.query(Employee,Department).outerjoin(Department)
for result in leftouter_join:
    print(result)
#right_outerjoin
right_outerjoin=session.query(Employee,Department).outerjoin(Employee)
for results in right_outerjoin:
    print(results)
#full_outerjoin
full_outerjoin=leftouter_join.union(right_outerjoin)
for output in full_outerjoin:
    print(output)


