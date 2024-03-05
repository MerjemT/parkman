import mysql.connector 
debug = False

class database():
  def __init__(self):
    from config import db as temp
    self.db = mysql.connector.connect(**temp)
    self.price = self.getConst("price")
    self.space = int(self.getConst("spaces"))

  def getConst(self, const):
    cursor = self.db.cursor()
    cursor.execute("SELECT const FROM constants where id=%(const)s",{"const":const})
    temp = cursor.fetchall()[0][0]
    cursor.close()
    return temp

  def __del__(self):
    self.db.close()

  def carEnter(self, licencePlate):
    cursor = self.db.cursor()
    querry = ("INSERT INTO parked "
              "(licence_plate, entrance_time) "
              "VALUES (%(lp)s, SYSDATE())")
    cursor.execute(querry, {"lp":licencePlate})
    self.db.commit()
    cursor.execute("SELECT entrance_time FROM parked WHERE id=LAST_INSERT_ID()")
    return cursor.fetchall()[0][0]
  
  def carExit(self, licencePlate):
    cursor = self.db.cursor()
    # get id of exiting car
    cursor.execute("SELECT id FROM parked WHERE licence_plate=%(lp)s AND exit_time IS NULL", {"lp":licencePlate})
    data = {"id":cursor.fetchall()[0][0]}

    # set exiting time 
    querry = ("UPDATE parked SET exit_time=SYSDATE() WHERE id=%(id)s ")
    if debug:
      querry = ("UPDATE parked SET exit_time='2021-05-15 09:04:34' where id=%(id)s;")
    cursor.execute(querry, data)

    # get elapsed time in parking
    cursor.execute("SELECT entrance_time, exit_time, TIME_TO_SEC(TIMEDIFF(exit_time, entrance_time))/3600 as time FROM parked where id=%(id)s ", data)
    times = cursor.fetchall()[0]

    self.db.commit()
    cursor.close()
    return times

  def getOccupiedSpacesNo(self):
    cursor = self.db.cursor()
    cursor.execute("SELECT count(id) FROM parked WHERE exit_time IS NULL")
    return cursor.fetchall()[0][0]

  def isIn(self, licencePlate):
    cursor = self.db.cursor()
    cursor.execute("SELECT count(id) FROM parked WHERE licence_plate=%(lp)s AND exit_time IS NULL", {"lp":licencePlate})
    return cursor.fetchall()[0][0] > 0


  def getAll(self):
    cursor = self.db.cursor()
    cursor.execute("select * from parked")
    for x in cursor:
      print(x)
    print()


if __name__ == "__main__":
  debug = True
  temp = database()
  print(temp.isIn("66057E4"))
  # print(temp.price)
  # temp.carEnter("test123")
  # print(temp.isIn("test123"))
  # # temp.getAll()
  # print(temp.getOccupiedSpacesNo())
  # print(temp.carExit("test123"))
  # print(temp.isIn("test123"))
  # temp.getAll()

