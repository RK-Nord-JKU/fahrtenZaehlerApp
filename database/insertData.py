from db_handler import DB_Handler, RD_Shift


if __name__ == '__main__':
    print("Run code")
    h = DB_Handler()
    h.createTable()

    filename = "database/statistic_202312.txt"
    file = open(filename, "r")
    while True:
        content=file.readline()
        if not content:
            break
        s = RD_Shift(*content.strip("\n").split(","))
        h.addShift(shift=s)
    file.close()