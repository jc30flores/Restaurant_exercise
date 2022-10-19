from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from tkinter import Button
from unicodedata import name
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from restdb_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurants.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = """"""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                                <input name="newRestaurantName" type="text" placeholder="New Restaurant Name">
                                <input type="submit" value="Create"> 
                            </form> </body></html>'''
                self.wfile.write(bytes(output, 'utf-8'))
                return

            if self.path.endswith("/edit_page"):
                id_restaurant = self.path.split("/")[2]
                restaurant_query = session.query(Restaurant).filter_by(id=id_restaurant).one()

                if restaurant_query:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = """"""
                    output += "<html><body>"
                    output += f"<h1> {restaurant_query.name} </h1>"
                    output += f'''<form method='POST' enctype='multipart/form-data' action='/restaurants/{id_restaurant}/edit_page'>
                                    <input name="newRestaurantName" type="text" placeholder= '{restaurant_query.name}' >
                                    <input type="submit" value="Rename"> 
                                </form> </body></html>'''
                    self.wfile.write(bytes(output, 'utf-8'))

            if self.path.endswith("/delete_page"):
                id_restaurant = self.path.split("/")[2]
                restaurant_query = session.query(Restaurant).filter_by(id=id_restaurant).one()

                if restaurant_query:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = """"""
                    output += "<html><body>"
                    output += f"<h1> Are you sure you want to delete {restaurant_query.name}? </h1>"
                    output += f'''<form method='POST' enctype='multipart/form-data' action='/restaurants/{id_restaurant}/delete_page'>
                                    <input type="submit" value="Delete"> 
                                </form> </body></html>'''
                    self.wfile.write(bytes(output, 'utf-8'))

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = """"""
                output += "<html><body>"
                output += "<a href='/restaurants/new'>Add New Restaurant Here</a></br></br>"
                restaurants = session.query(Restaurant).all()
                for r in restaurants:
                    output += f"""{r.name}</br>
                            <a href='/restaurants/{r.id}/edit_page'>Edit</a></br>
                            <a href='/restaurants/{r.id}/delete_page'>Delete</a>
                            </br></br></br>"""
                output += "</body></html>"
                self.wfile.write(bytes(output, 'utf-8'))
                return

           
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)



    def do_POST(self):

        if self.path.endswith('/edit_page'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')
                id_restaurant = self.path.split("/")[2]
                restaraunt_query = session.query(Restaurant).filter_by(id=id_restaurant).one()

                if restaraunt_query != []:
                    print(restaraunt_query.name)
                    restaraunt_query.name = messagecontent[0]
                    #session.add(restaraunt_query)
                    #session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    print(restaraunt_query.name)

        if self.path.endswith('/delete_page'):
            id_restaurant = self.path.split("/")[2]
            restaraunt_query = session.query(Restaurant).filter_by(id=id_restaurant).one()
            if restaraunt_query != []:
                session.delete(restaraunt_query)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                print(f"Deleting this restaurant {restaraunt_query.name}")


        if self.path.endswith('/restaurants/new'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')

                #Create new Restaurant Object
                newRestaurant = Restaurant(name=messagecontent[0])
                session.add(newRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

        

                
        



def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()