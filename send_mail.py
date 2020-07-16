#!/usr/bin/env python3
# coding: utf-8

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
import smtplib
#from test import _mail
#==============================================
def go(entry, label):
    label.set_text(entry.get_text())
    entry.set_text('Already imported')
#==============================================
path = None
mails = None


def _m(to, subject, message):
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.login('mail@gmail.com', 'password or pass for APP') # to get it
    smtp_server.sendmail('mail@gmail.com', '{}'.format(to), 'Subject: {}!\n{}'.format(subject, message))

    print('Email sent successfully')

def _s(entry, e1, e2, e3):
    e = [e1.get_text(), e2.get_text(), getText(e3)]
    global mails
    global path
    global pb
    global l_
    i = 1
    print(path)
    if "@" in e[0]:
        mails = e[0]
        _m(mails, e[1], e[2])
        l_.set_text("Message sent successfully {}/{}!".format(1,1))
        pb.set_fraction(float("{:.2}".format(1/1)))
    else:
        for elt in mails:
            _m(elt, e[1], e[2])
            l_.set_text("Message sent successfully {}/{}!".format(i,len(mails)))
            pb.set_fraction(float("{:.2}".format(i/len(mails))))
            i += 1


def labels(fname):
    # read label and remove '\n' at the end of eah line
    with open("{}".format(fname)) as filename:
        lines = [line.rstrip() for line in filename]
    return lines

def total_mail(entry, label):
    global path
    global mails
    dia = Gtk.FileChooserDialog("Choose a file", None,
        Gtk.FileChooserAction.OPEN,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
         Gtk.STOCK_OPEN, Gtk.ResponseType.OK))


    response = dia.run()

    if response == Gtk.ResponseType.OK:
        print("Open clicked")
        print("File selected: " + dia.get_filename())
        path = dia.get_filename()
    elif response == Gtk.ResponseType.CANCEL:
        print("Cancel clicked")

    _list = labels(path)
    label.set_text("{} adresses mails".format(len(_list)))
    mails = _list

    dia.destroy()
    mails = _list

def getText(textview):
    buffer = textview.get_buffer()
    startIter, endIter = buffer.get_bounds()
    text = buffer.get_text(startIter, endIter, False)
    return text


if __name__ == "__main__":
    c = 0

    window = Gtk.Window()
    window.set_title("Email Sender Tagus Drone")
    window.set_border_width(200)
    window.connect('delete-event', Gtk.main_quit)
    #grid = Gtk.Grid()
    grid = Gtk.Grid()
    grid.set_row_spacing(10)
    grid.set_column_spacing(10)
    #grid.set_row_homogeneous(True)
    #grid.set_column_homogeneous(True)
#==================================
    #
    #pixbuf = pixbuf.scale_simple(80, 80, GdkPixbuf.InterpType.BILINEAR)


    l_to = Gtk.Label()
    l_to.set_text("Destinataire(s)")
    entry = Gtk.Entry()
    entry.set_text("@gmail.com")
    btn_import = Gtk.Button(label="Import file")
    btn_import.connect("clicked", total_mail, entry)

    grid.attach(l_to, 0, 1, 1, 1)
    grid.attach(entry, 1, 1, 2, 1)
    grid.attach(btn_import, 3, 1, 1, 1)

    l_object = Gtk.Label()
    l_object.set_text("Object")
    e_object = Gtk.Entry()

    grid.attach(l_object, 0, 2, 1, 1)
    grid.attach(e_object, 1, 2, 5, 1)

    l_body = Gtk.Label()
    l_body.set_text("Message")
    e_body = Gtk.TextView()


    grid.attach(l_body, 0, 3, 1, 1)
    grid.attach(e_body, 1, 3, 5, 20)

    pb = Gtk.ProgressBar()
    pb.set_fraction(0)

    grid.attach(pb, 0, 24, 10, 1)

    l_ = Gtk.Label()
    l_.set_text("") #Message(s) envoyé(s) avec succès !

    grid.attach(l_, 1, 25, 1, 1)

    btn_send = Gtk.Button(label="Send")
    btn_send.connect("clicked", _s, entry, e_object, e_body)

    grid.attach(btn_send, 3, 23, 1, 1)



    window.add(grid)
    window.show_all()
    Gtk.main()
