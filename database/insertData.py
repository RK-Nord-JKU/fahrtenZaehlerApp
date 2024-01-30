from db_handler import DB_Handler, RD_Shift
from datetime import date

# if __name__ == '__main__':
#     print("Run code")
h = DB_Handler()
df = h.selectDF()
print(df)
df.head()
#     h.createTable()

#     filename = "database/statistic_202312.txt"
#     file = open(filename, "r")
#     while True:
#         content=file.readline()
#         if not content:
#             break
#         s = RD_Shift(*content.strip("\n").split(","))
#         h.addShift(shift=s)
#     file.close()