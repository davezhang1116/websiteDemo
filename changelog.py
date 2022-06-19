from dataclasses import dataclass
import sqlite3


@dataclass
class changelog:

    _ID:int
    _name:str= None
    _initialBalance:float= None
    _finalBalance:float= None
    _type:str= None
    _time:str= None

    def __init__(self, _ID, _name= None, _initialBalance= None, _finalBalance= None,_type= None,_time= None):
        self.ID = _ID
        self.name = _name
        self.initialBalance = _initialBalance
        self.finalBalance = _finalBalance
        self.type = _type
        self.time = _time

    def create(self):
        conn = sqlite3.connect('./database/history.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE {} (
        task_num INTEGER PRIMARY KEY AUTOINCREMENT,
        id INTEGER,
        name TEXT,
        initialBalance REAL,
        finalBalance REAL,
        type TEXT,
        time TEXT

        )""".format("task"+str(self.ID)))
        conn.commit()
        conn.close()


    def store(self):
        conn = sqlite3.connect('./database/history.db')
        c = conn.cursor()
        #c.execute("""INSERT INTO {} (id, name, initialBalance, finalBalance, type, time) VALUES ({},'{}',{},{},{},'{}')
        #""".format("task"+str(self.ID), self.ID, self.name, self.initialBalance, self.finalBalance, self.type, self.time))
        parms = (self.ID, self.name, self.initialBalance, self.finalBalance, self.type, self.time)
        c.execute("""INSERT INTO {} VALUES (NULL, ?, ?, ?, ?, ?, ?)""".format("task"+str(self.ID)),parms)

        conn.commit()
        conn.close()

    def read(self):
        conn = sqlite3.connect('./database/history.db')
        c = conn.cursor()
        c.execute("""SELECT * FROM {}""".format("task"+str(self.ID)))
        list = c.fetchall()
        added_on = ""
        for info in list:
            id = info[1]
            name = info[2]
            initialBalance = info[3]
            finalBalance = info[4]
            type = info[5]
            time = info[6]
            change_in_balance = finalBalance - initialBalance

            added_on = added_on + """
            <tr>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>

            </tr>

            """.format(id,name,"{:.2f}".format(initialBalance),"{:.2f}".format(finalBalance),type,time,"{:.2f}".format(change_in_balance))



        html_code = """
        <head>
        <link rel="stylesheet" href="/static/css/main.css">
        </head>
        <div class="content">
            <h1 style="text-align: center">MONEY</h1>
                <input type="text" id="input" onkeyup="search()" placeholder="Search for dates.." title="Type in a date">

                <table id="list">
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Initial Balance</th>
                        <th>Final Balance</th>
                        <th>Type</th>
                        <th>Time</th>
                        <th>Change In Balance</th>
                    </tr>

                    """+added_on+"""

                </table>

                <script>
                function search() {
                  var input, filter, table, tr, td, i, txtValue;
                  input = document.getElementById("input");
                  filter = input.value.toUpperCase();
                  table = document.getElementById("list");
                  tr = table.getElementsByTagName("tr");
                  for (i = 0; i < tr.length; i++) {
                    td = tr[i].getElementsByTagName("td")[5];
                    if (td) {
                      txtValue = td.textContent || td.innerText;
                      if (txtValue.toUpperCase().indexOf(filter) > -1) {
                        tr[i].style.display = "";
                      } else {
                        tr[i].style.display = "none";
                      }
                    }
                  }
                }
                </script>
            </div>
        </div>
        """

        return html_code
