import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,QLabel,
                             QHBoxLayout,QGridLayout,QPushButton,QLineEdit,QSlider, 
                             QComboBox,QCheckBox,QColorDialog,QFileDialog,QStackedWidget,QMessageBox)
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import QIcon
import numpy as np
import pyqtgraph as pg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from fpdf import FPDF
import scipy.interpolate as interp
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import numpy as np
import time
import threading
from glueSignals import GlueSignalsWindow
import os
from datetime import datetime


class SignalViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signal viewer")
        self.setGeometry(200,200,1500,1200)

        # declaration of graph1 and its attributes
        self.graph1=QWidget()
        self.start_button1 = QPushButton()
        self.start_button1.setIcon(QIcon(".venv/images/pause.png"))
        self.zoom_in_button1 = QPushButton()
        self.zoom_in_button1.setIcon(QIcon(".venv/images/zoom-in.png")) 
        self.zoom_out_button1 = QPushButton()
        self.zoom_out_button1.setIcon(QIcon(".venv/images/zoom-out.png")) 
        self.manual_zoom1=False
        self.rewind_button1 = QPushButton()
        self.rewind_button1.setIcon(QIcon(".venv/images/rewind.png")) 
        self.signal_list1 = []  # To store multiple signals for Graph 1
        self.t_list1 = []  # To store time values for each signal
        self.current_indices1 = []  # To track the current index for each signal in the animation
        self.timer1 = QTimer()  # Timer for animation
        self.timer1.timeout.connect(self.update_animation1)  # Connect timer to update method
        self.window_size1 = 100  # Number of points in the moving window

        # declaration of controls of graph1 
        self.controls1=QWidget()
        self.select_label1=QLabel("Select signal:")
        self.select_signal1=QComboBox()
        self.edit_label1=QLabel("Edit signal name:")
        self.edit_signal_name1=QLineEdit()
        self.signal_names1 = []  # Store names of the signals
        self.visibility_checkbox1=QCheckBox("Visibility")
        self.signal_visibility1 = []  # Store visibility state for each signal
        self.color_button1 = QPushButton("Select Color")
        self.signal_colors1 = []  # Store colors for each signal
        self.speed_label1 = QLabel("Signal speed")
        self.speed_slider1 = QSlider(Qt.Horizontal)
        self.signals_speed1 =1
        self.browse_button1 = QPushButton("Browse file")
        self.move_signal_button1 = QPushButton("Move to graph 2")
        self.real_signal_button1 = QPushButton("Start real signal")
        self.real_t=[]
        self.real_signal=[]
        self.is_fetching_real_time=False
       
        # declaration of link buttons
        self.link_graphs=QPushButton("Link graphs")
        self.link_pause=QPushButton()
        self.link_pause.hide()
        self.link_pause.setIcon(QIcon(".venv/images/pause.png"))
        self.link_zoom_in=QPushButton()
        self.link_zoom_in.hide()
        self.link_zoom_in.setIcon(QIcon(".venv/images/zoom-in.png"))
        self.link_zoom_out=QPushButton()
        self.link_zoom_out.hide()
        self.link_zoom_out.setIcon(QIcon(".venv/images/zoom-out.png"))
        self.link_rewind = QPushButton()
        self.link_rewind.hide()
        self.link_rewind.setIcon(QIcon(".venv/images/rewind.png"))
        self.graphs_linked = False

        self.next_page_button=QPushButton("Non-rectangular Graph")


        # declaration of graph2 and its attributes
        self.graph2=QWidget()
        self.start_button2 = QPushButton()
        self.start_button2.setIcon(QIcon(".venv/images/pause.png"))
        self.zoom_in_button2 = QPushButton()
        self.zoom_in_button2.setIcon(QIcon(".venv/images/zoom-in.png")) 
        self.zoom_out_button2 = QPushButton()
        self.zoom_out_button2.setIcon(QIcon(".venv/images/zoom-out.png")) 
        self.manual_zoom2=False
        self.rewind_button2 = QPushButton()
        self.rewind_button2.setIcon(QIcon(".venv/images/rewind.png")) 
        self.signal_list2 = []  # To store multiple signals for Graph 1
        self.t_list2 = []  # To store time values for each signal
        self.current_indices2 = []  # To track the current index for each signal in the animation
        self.timer2 = QTimer()  # Timer for animation
        self.timer2.timeout.connect(self.update_animation2)  # Connect timer to update method
        self.window_size2 = 100  # Number of points in the moving window


        # declaration of controls of graph2
        self.controls2=QWidget()
        self.select_label2=QLabel("Select signal:")
        self.select_signal2=QComboBox()
        self.signal_names2= []  # Store names of the signals
        self.edit_label2=QLabel("Edit signal name:")
        self.edit_signal_name2=QLineEdit()
        self.visibility_checkbox2=QCheckBox("Visibility")
        self.signal_visibility2 = []  # Store visibility state for each signal
        self.color_button2 = QPushButton("Select Color")
        self.signal_colors2 = []  # Store colors for each signal
        self.speed_label2 = QLabel("Signal speed")
        self.speed_slider2 = QSlider(Qt.Horizontal)
        self.signals_speed2 = 1
        self.browse_button2 = QPushButton("Browse file")
        self.move_signal_button2 = QPushButton("Move to graph 1")
        self.real_signal_button2 = QPushButton("Browse real signal")

        # declaration of glue graph
        self.graph3=QWidget()
        self.snapshot_button=QPushButton()
        self.generate_pdf_button=QPushButton()
        self.generate_pdf_button.setIcon(QIcon(".venv/images/pdf-report.png"))
        self.snapshot_button.setIcon(QIcon(".venv/images/screenshot.png"))
        self.glue_controls=QWidget()
        self.window_start1=QLabel("Window start (signal 1):")
        self.window_start1_textbox=QLineEdit()
        self.window_start2=QLabel("Window start (signal 2):")
        self.window_start2_textbox=QLineEdit()
        self.glue_size1=QLabel("Window size (signal 1):")
        self.glue_size1_textbox=QLineEdit()
        self.glue_size2=QLabel("Window size (signal 2):")
        self.glue_size2_textbox=QLineEdit()
        self.gap_label=QLabel("Gap:")
        self.gap_textbox=QLineEdit()
        # self.overlap=QLabel("Overlap:")
        # self.overlap_textbox=QLineEdit()
        self.interpolation=QLabel("Interpolation order:")
        self.interpolation_textbox=QLineEdit()
        self.glue_signals_button=QPushButton("Glue signals")
        self.snapshots=[]


        # Initialize arrays for time and price data
        self.real_time_y = []
        self.real_time_x = []
        self.real_signal_timer=QTimer()

        self.second_page_opened=False
        


        # the initialization of the UI
        self.initUi()



    def initUi(self):
        self.stacked_widget=QStackedWidget()
        # creating the main window
        self.main_widget=QWidget()
        container=QGridLayout()
        self.main_widget.setLayout(container) # put the container in the main_window

        self.new_page=QWidget()
        self.stacked_widget.addWidget(self.main_widget)
        self.stacked_widget.addWidget(self.new_page)
        self.stacked_widget.setCurrentWidget(self.main_widget)
        self.setCentralWidget(self.stacked_widget)


        # graph1
        self.graph1_layout=QVBoxLayout()

        #the first part is for buttons
        group_buttons_layout1=QHBoxLayout()
        group_buttons_layout1.addWidget(self.start_button1)
        group_buttons_layout1.addWidget(self.zoom_in_button1)
        group_buttons_layout1.addWidget(self.zoom_out_button1)
        group_buttons_layout1.addWidget(self.rewind_button1)
        group_buttons_layout1.setAlignment(Qt.AlignLeft)
        # the second part is for the graph
        self.canvas1=self.create_signal_canvas1()
        self.graph1_layout.addLayout(group_buttons_layout1)
        self.graph1_layout.addWidget(self.canvas1)
        self.graph1.setLayout(self.graph1_layout)


        container.addWidget(self.graph1,0,0) # graph1 section in the first row and first column of the grid

        self.start_button1.clicked.connect(self.pause_signal1)   #ana seifo aho lesa mezawed el heta 3  a 
        self.zoom_in_button1.clicked.connect(self.zoom_in_signal1)
        self.zoom_out_button1.clicked.connect(self.zoom_out_signal1)
        self.rewind_button1.clicked.connect(self.rewind_signal1)

        
        # controls1
        controls1_layout=QVBoxLayout()

        select_layout1=QHBoxLayout()
        select_layout1.addWidget(self.select_label1)
        select_layout1.addWidget(self.select_signal1)
        self.select_signal1.currentIndexChanged.connect(self.on_signal_selected1)
       
        

        edit_layout1=QHBoxLayout()
        edit_layout1.addWidget(self.edit_label1)
        edit_layout1.addWidget(self.edit_signal_name1)
        self.edit_signal_name1.returnPressed.connect(self.update_signal_name1)  # Edit signal name when enter is pressed

        

        color_layout1=QHBoxLayout()
        color_layout1.addWidget(self.visibility_checkbox1)
        self.visibility_checkbox1.stateChanged.connect(self.update_signal_visibility1)
        color_layout1.addWidget(self.color_button1)
        self.color_button1.clicked.connect(self.select_color)
        

        speed_layout1=QHBoxLayout()
        speed_layout1.addWidget(self.speed_label1)
        speed_layout1.addWidget(self.speed_slider1)
        self.speed_slider1.valueChanged.connect(self.update_signal_speed1)

        file_layout1=QHBoxLayout()
        file_layout1.addWidget(self.browse_button1)
        self.browse_button1.clicked.connect(self.load_signals_for_graph1)
        file_layout1.addWidget(self.move_signal_button1)
        self.move_signal_button1.clicked.connect(self.move_signal_to_graph2)

        controls1_layout.addLayout(select_layout1)
        controls1_layout.addLayout(edit_layout1)
        controls1_layout.addLayout(color_layout1)
        controls1_layout.addLayout(speed_layout1)
        controls1_layout.addLayout(file_layout1)
        self.controls1.setLayout(controls1_layout)
        self.controls1.setFixedHeight(280)
        container.addWidget(self.controls1,0,1) # controls1 section in the first row and and second column in the grid


        # Link buttons
        link_buttons=QWidget()
        link_buttons_layout=QHBoxLayout()
        link_buttons_layout.addWidget(self.link_pause)
        link_buttons_layout.addWidget(self.link_zoom_in)
        link_buttons_layout.addWidget(self.link_zoom_out)
        link_buttons_layout.addWidget(self.link_rewind)
        link_buttons_layout.addWidget(self.link_graphs)
        self.link_graphs.clicked.connect(self.link_graphs_function)
        link_buttons_layout.setAlignment(Qt.AlignRight)
        link_buttons.setLayout(link_buttons_layout)
        container.addWidget(link_buttons,1,0)

        self.link_pause.clicked.connect(self.pause_linked_signals)  
        self.link_zoom_in.clicked.connect(self.zoom_in_linked_signals)
        self.link_zoom_out.clicked.connect(self.zoom_out_linked_signals)  
        self.link_rewind.clicked.connect(self.rewind_linked_signals)

        next_page=QWidget()
        next_page_button_layout=QHBoxLayout()
        next_page_button_layout.addWidget(self.next_page_button)
        next_page_button_layout.setAlignment(Qt.AlignRight)
        next_page.setLayout(next_page_button_layout)
        container.addWidget(next_page,1,1)
        self.next_page_button.clicked.connect(self.open_new_page)


        # graph 2
        self.graph2_layout=QVBoxLayout()
        #the first part is for buttons
        group_buttons_layout2=QHBoxLayout()
        group_buttons_layout2.addWidget(self.start_button2)
        group_buttons_layout2.addWidget(self.zoom_in_button2)
        group_buttons_layout2.addWidget(self.zoom_out_button2)
        group_buttons_layout2.addWidget(self.rewind_button2)
        group_buttons_layout2.setAlignment(Qt.AlignLeft)
        #the second part is for the graph
        self.canvas2=self.create_signal_canvas2()

        self.graph2_layout.addLayout(group_buttons_layout2)
        self.graph2_layout.addWidget(self.canvas2)
        self.graph2.setLayout(self.graph2_layout)
        container.addWidget(self.graph2,2,0) # graph2 section in the second row and first column in grid

        self.start_button2.clicked.connect(self.pause_signal2)   #ana seifo aho lesa mezawed el heta di 
        self.zoom_in_button2.clicked.connect(self.zoom_in_signal2)
        self.zoom_out_button2.clicked.connect(self.zoom_out_signal2)
        self.rewind_button2.clicked.connect(self.rewind_signal2)

        # controls 2
        controls2_layout=QVBoxLayout()

        select_layout2=QHBoxLayout()
        select_layout2.addWidget(self.select_label2)
        select_layout2.addWidget(self.select_signal2)
        self.select_signal2.currentIndexChanged.connect(self.on_signal_selected2)

        edit_layout2=QHBoxLayout()
        edit_layout2.addWidget(self.edit_label2)
        edit_layout2.addWidget(self.edit_signal_name2)
        self.edit_signal_name2.returnPressed.connect(self.update_signal_name2)  # Edit signal name when enter is pressed

        color_layout2=QHBoxLayout()
        color_layout2.addWidget(self.visibility_checkbox2)
        self.visibility_checkbox2.stateChanged.connect(self.update_signal_visibility2)
        color_layout2.addWidget(self.color_button2)
        self.color_button2.clicked.connect(self.select_color)

        speed_layout2=QHBoxLayout()
        speed_layout2.addWidget(self.speed_label2)
        speed_layout2.addWidget(self.speed_slider2)
        self.speed_slider2.valueChanged.connect(self.update_signal_speed2)

        file_layout2=QHBoxLayout()
        file_layout2.addWidget(self.browse_button2)
        self.browse_button2.clicked.connect(self.load_signals_for_graph2)
        file_layout2.addWidget(self.move_signal_button2)
        self.move_signal_button2.clicked.connect(self.move_signal_to_graph1)
        # file_layout2.addWidget(self.real_signal_button2)

        controls2_layout.addLayout(select_layout2)
        controls2_layout.addLayout(edit_layout2)
        controls2_layout.addLayout(color_layout2)
        controls2_layout.addLayout(speed_layout2)
        controls2_layout.addLayout(file_layout2)
        self.controls2.setLayout(controls2_layout)
        # self.controls2.setStyleSheet("background-color:red;")
        self.controls2.setFixedHeight(280)
        container.addWidget(self.controls2,2,1)  # controls 2 in the second row and ssecond column in grid



        # Glue graph
        
        graph3_layout=QVBoxLayout()
        images_layout=QHBoxLayout()
        images_layout.addWidget(self.snapshot_button)
        images_layout.addWidget(self.generate_pdf_button)
        graph3_layout.addLayout(images_layout)
        self.generate_pdf_button.clicked.connect(self.generate_pdf_report)
        self.snapshot_button.clicked.connect(self.snapshot_graph3)
        self.canvas3=self.create_signal_canvas3()
        graph3_layout.addWidget(self.canvas3)
        self.graph3.setLayout(graph3_layout)
        container.addWidget(self.graph3,3,0)

        # Glue controls
        
        window_start1_layout=QHBoxLayout()
        window_start1_layout.addWidget(self.window_start1)
        window_start1_layout.addWidget(self.window_start1_textbox)
        glue_size1_layout=QHBoxLayout()
        glue_size1_layout.addWidget(self.glue_size1)
        glue_size1_layout.addWidget(self.glue_size1_textbox)
        window_start2_layout=QHBoxLayout()
        window_start2_layout.addWidget(self.window_start2)
        window_start2_layout.addWidget(self.window_start2_textbox)
        glue_size2_layout=QHBoxLayout()
        glue_size2_layout.addWidget(self.glue_size2)
        glue_size2_layout.addWidget(self.glue_size2_textbox)
        # gap_overlap_layout=QHBoxLayout()
        # gap_overlap_layout.addWidget(self.gap_label)
        # gap_overlap_layout.addWidget(self.gap_textbox)
        # self.gap_textbox.textChanged.connect(self.update_glue_window_gap) 
        # overlap_layout=QHBoxLayout()
        # overlap_layout.addWidget(self.overlap)
        # overlap_layout.addWidget(self.overlap_textbox)
        interpolation_layout=QHBoxLayout()
        interpolation_layout.addWidget(self.interpolation)
        interpolation_layout.addWidget(self.interpolation_textbox)
        glue_controls_layout=QVBoxLayout()
        # glue_controls_layout.addLayout(gap_overlap_layout)
        glue_button_layout=QHBoxLayout()
        glue_button_layout.addWidget(self.glue_signals_button)
        glue_button_layout.addWidget(self.real_signal_button1)
        # glue_controls_layout.addLayout(overlap_layout)
        # glue_controls_layout.addLayout(interpolation_layout)
        glue_controls_layout.addLayout(glue_button_layout)
        self.real_signal_button1.clicked.connect(self.start_real_time_signal)
        self.glue_signals_button.clicked.connect(self.open_glue_signals_window)
        self.glue_controls.setLayout(glue_controls_layout)
        container.addWidget(self.glue_controls,3,1)
    
        container.setColumnStretch(0,2)
        container.setColumnStretch(1,1)

        # Styling

        # setting the width of buttons and other controls
        self.speed_slider1.setMaximumWidth(300)
        self.speed_slider2.setMaximumWidth(300)
        self.select_signal1.setFixedWidth(300)
        self.edit_signal_name1.setMaximumWidth(300)
        self.edit_signal_name2.setMaximumWidth(300)
        self.browse_button1.setMaximumWidth(150)
        self.move_signal_button1.setMaximumWidth(150)
        self.browse_button2.setMaximumWidth(150)
        self.move_signal_button2.setMaximumWidth(150)
        self.color_button1.setMaximumWidth(150)
        self.color_button2.setMaximumWidth(150)
        self.start_button1.setMaximumWidth(50)
        self.zoom_in_button1.setMaximumWidth(50)
        self.zoom_out_button1.setMaximumWidth(50)
        self.rewind_button1.setMaximumWidth(50)
        self.start_button2.setMaximumWidth(50)
        self.zoom_in_button2.setMaximumWidth(50)
        self.zoom_out_button2.setMaximumWidth(50)
        self.rewind_button2.setMaximumWidth(50)
        self.link_rewind.setMaximumWidth(50)
        self.link_pause.setMaximumWidth(50)
        self.link_zoom_out.setMaximumWidth(50)
        self.link_zoom_in.setMaximumWidth(50)
        self.link_graphs.setMaximumWidth(130)
        self.next_page_button.setMaximumWidth(175)
        self.snapshot_button.setMaximumWidth(50)
        self.generate_pdf_button.setMaximumWidth(50)
        self.glue_signals_button.setMaximumWidth(130)
        self.real_signal_button1.setMaximumWidth(150)
    

        self.setStyleSheet("""
            QWidget{
                    background-color: #28292b;
            }               
            QLabel{
                    font-size:20px;  
                    color:white;
                        }
            QCheckBox{
                           font-size:20px;}
            QPushButton{
                    font-size:15px;
                    padding:10px;
                    border:white 1px solid;
                    border-radius:15px;
                    background-color:white;
                    color:black;       
                           }               
        """)


       

    # creating the canvas for plotting signals
    def create_signal_canvas1(self):

        # Pass the custom ViewBox to the PlotWidget
        plot_widget1 = pg.PlotWidget()
        # plot_widget1 = pg.PlotWidget()
        plot_widget1.setBackground('k')
        

        plot_widget1.showGrid(x=True, y=True, alpha=0.3)
        plot_widget1.setXRange(0,0.9)
        plot_widget1.setYRange(-0.8,0.8)

        plot_widget1.setLimits(xMin=0)
        plot_widget1.setLimits(xMax=0.64)

        return plot_widget1

    def create_signal_canvas2(self):
        plot_widget2 = pg.PlotWidget()
        plot_widget2.setBackground('k')

        plot_widget2.showGrid(x=True, y=True, alpha=0.3)
        plot_widget2.setXRange(0, 0.9)
        plot_widget2.setYRange(-0.8, 0.8)
        plot_widget2.setLimits(xMin=0)
        plot_widget2.setLimits(xMax=0.64)
        plot_widget2.setLimits(yMin=-1.5)
        plot_widget2.setLimits(yMax=1.5)
        return plot_widget2
    
    def create_signal_canvas3(self):
        plot_widget3 = pg.PlotWidget()
        plot_widget3.setBackground('k')

        plot_widget3.showGrid(x=True, y=True, alpha=0.3)
        plot_widget3.setXRange(0, 0.9)
        plot_widget3.setYRange(-0.8, 0.8)

        return plot_widget3
    

    #changing the color of the signals
    def select_color(self):

        # Open a color dialog and allow the user to pick a color
        color = QColorDialog.getColor()

        if color.isValid():
            # Convert QColor to Matplotlib's RGB format
            rgb_color = color.name()  # Get the color as a hex string

            button=self.sender()

            if button==self.color_button1:
                # Update the color for the selected signal
                selected_index = self.select_signal1.currentIndex()
                if selected_index >= 0:
                    self.signal_colors1[selected_index] = rgb_color  # Update color list

                    # Immediately update the plot to reflect the new color
                    self.update_animation1()

            elif button==self.color_button2:
                # Update the color for the selected signal
                selected_index = self.select_signal2.currentIndex()
                if selected_index >= 0:
                    self.signal_colors2[selected_index] = rgb_color  # Update color list

                    # Immediately update the plot to reflect the new color
                    self.update_animation2()

    def load_signals_for_graph1(self):
        # Open a file dialog to select multiple files
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Select Signal Files", "", "All Files (*);;CSV Files (*.csv)", options=options)
        
        if files:
            for file in files:
                self.add_signal_to_graph1(file)
                # Start animation after loading signals
                self.start_animation1()

    def add_signal_to_graph1(self, file_path):
        # Assume file is a CSV where the first column is time and the second column is signal data
        data = np.loadtxt(file_path, delimiter=',')  # Example for loading CSV data
        t = data[:, 0]  # Time values
        signal = data[:, 1]  # Signal values

        self.t_list1.append(t)
        self.signal_list1.append(signal)
        self.current_indices1.append(0)  # Start each signal's index at 0
        default_name = f"Graph1_Signal {len(self.signal_names1) + 1}"
        self.signal_names1.append(default_name)
        self.signal_colors1.append('#ff0000')  # Default color red
        self.signal_visibility1.append(True)  # Default visibility is True

        # Add the signal's name to the select menu
        self.select_signal1.addItem(default_name)
        self.rewind_signal1()

    def start_animation1(self):
        self.timer1.start(210)  # Start the timer with the desired speed


    def update_animation1(self):

        # Variable to track the overall min and max signal values for dynamic Y-axis scaling
        min_signal, max_signal = float('inf'), float('-inf')

        for i, (t, signal) in enumerate(zip(self.t_list1, self.signal_list1)):
            index = self.current_indices1[i]

            # Increment the index based on the signal's speed factor
            self.current_indices1[i] += self.signals_speed1

            if self.signal_visibility1[i]:  # Check if the signal is visible
                if index < len(t):  # If index is within the range of the signal data
                    # Define the range for the moving window (for X-axis)
                    start_index = max(0, index - self.window_size1)
                    end_index = index

                    # Check if the current window has data
                    if start_index < end_index:  # Avoid processing an empty slice
                        # Plot the portion of the signal within the window
                        pen = pg.mkPen(color=self.signal_colors1[i], width=2)
                        self.canvas1.plot(t[start_index:end_index], signal[start_index:end_index], pen=pen)

                        # Track the min and max signal values for the current window (Y-axis scaling)
                        min_signal = min(min_signal, np.min(signal[start_index:end_index]))
                        max_signal = max(max_signal, np.max(signal[start_index:end_index]))
                        self.canvas1.setLimits(yMin=min_signal-0.07)
                        self.canvas1.setLimits(yMax=max_signal+0.07)

                        self.canvas1.setXRange(t[start_index], t[end_index], padding=0)
                        # self.canvas1.setLimits(xMax=t[end_index])

                else:
                    # If signal is done, plot the entire signal to finish
                    pen = pg.mkPen(color=self.signal_colors1[i], width=2)
                    self.current_indices1[i] = len(t)
                    self.canvas1.plot(t, signal, pen=pen)
        # Automatically adjust Y-axis only if no manual zoom occurred
        if not self.manual_zoom1:
            # Set Y-axis to show the whole signal's range
            if min_signal < float('inf') and max_signal > float('-inf'):
                self.canvas1.setYRange(min_signal - 0.1 * abs(min_signal), max_signal + 0.1 * abs(max_signal), padding=0.1)

        # Stop animation when all signals are fully displayed
        if all(index >= len(t) for index, t in zip(self.current_indices1, self.t_list1)):
            self.timer1.stop()
            

    def load_signals_for_graph2(self):
        # Open a file dialog to select multiple files
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Select Signal Files", "", "All Files (*);;CSV Files (*.csv)", options=options)
        
        if files:
            for file in files:
                self.add_signal_to_graph2(file)
                # Start animation after loading signals
                self.start_animation2()

    def add_signal_to_graph2(self, file_path):
        # Assume file is a CSV where the first column is time and the second column is signal data
        data = np.loadtxt(file_path, delimiter=',')  # Example for loading CSV data
        t = data[:, 0]  # Time values
        signal = data[:, 1]  # Signal values

        self.t_list2.append(t)
        self.signal_list2.append(signal)
        self.current_indices2.append(0)  # Start each signal's index at 0
        default_name = f"Graph2_Signal {len(self.signal_names2) + 1}"
        self.signal_names2.append(default_name)
        self.signal_colors2.append('#ff0000')  # Default color red
        self.signal_visibility2.append(True)  # Default visibility is True

        # Add the signal's name to the select menu
        self.select_signal2.addItem(default_name)
        self.rewind_signal2()

    def start_animation2(self):
        self.timer2.start(210)  # Start the timer with the desired speed

    def update_animation2(self):
        # self.canvas2.clear()  # Clear the previous plot
        # Variable to track the overall min and max signal values for dynamic Y-axis scaling
        min_signal, max_signal = float('inf'), float('-inf')

        for i, (t, signal) in enumerate(zip(self.t_list2, self.signal_list2)):
            index = self.current_indices2[i]

            self.current_indices2[i] +=self.signals_speed2


            if self.signal_visibility2[i]:
                # If index is within the range of the signal data
                if index < len(t):
                    # Define the range for the moving window
                    start_index = max(0, index - self.window_size2)
                    end_index = index

                    # Check if the current window has data
                    if start_index < end_index:  # Avoid processing an empty slice
                        # Plot the portion of the signal within the window
                        pen = pg.mkPen(color=self.signal_colors2[i], width=2)
                        self.canvas2.plot(t[start_index:end_index], signal[start_index:end_index], pen=pen)

                        # Track the min and max signal values for the current window (Y-axis scaling)
                        min_signal = min(min_signal, np.min(signal[start_index:end_index]))
                        max_signal = max(max_signal, np.max(signal[start_index:end_index]))
                        self.canvas2.setLimits(yMin=min_signal-0.07)
                        self.canvas2.setLimits(yMax=max_signal+0.07)

                        self.canvas2.setXRange(t[start_index], t[end_index], padding=0)
                        
                        # self.canvas2.setLimits(xMax=t[end_index])
                else:
                    # Stop the signal if it has reached the end
                    pen = pg.mkPen(color=self.signal_colors2[i], width=2)
                    self.current_indices2[i] = len(t)
                    self.canvas2.plot(t, signal, pen=pen)
        # Automatically adjust Y-axis only if no manual zoom occurred
        if not self.manual_zoom2:
            # Set Y-axis to show the whole signal's range
            if min_signal < float('inf') and max_signal > float('-inf'):
                self.canvas2.setYRange(min_signal - 0.1 * abs(min_signal), max_signal + 0.1 * abs(max_signal), padding=0.1)

        # Check if all signals are done
        if all(index >= len(t) for index, t in zip(self.current_indices2, self.t_list2)):
            self.timer2.stop()  # Stop animation when all signals are fully displayed

    def on_signal_selected1(self):
        # When the user selects a signal, display its name in the edit textbox
        selected_index = self.select_signal1.currentIndex()
        if selected_index >= 0:
            self.edit_signal_name1.setText(self.signal_names1[selected_index])

            # Set the visibility checkbox to the signal's current visibility
            self.visibility_checkbox1.setChecked(self.signal_visibility1[selected_index])

    def update_signal_name1(self):
        # Update the selected signal's name based on the content of the edit textbox
        selected_index = self.select_signal1.currentIndex()
        new_name = self.edit_signal_name1.text()

        if selected_index >= 0 and new_name:
            # Update the name in the signal_names list
            self.signal_names1[selected_index] = new_name

            # Update the name in the select menu
            self.select_signal1.setItemText(selected_index, new_name)

    def on_signal_selected2(self):
        # When the user selects a signal, display its name in the edit textbox
        selected_index = self.select_signal2.currentIndex()
        if selected_index >= 0:
            self.edit_signal_name2.setText(self.signal_names2[selected_index])

            # Set the visibility checkbox to the signal's current visibility
            self.visibility_checkbox2.setChecked(self.signal_visibility2[selected_index])

    def update_signal_name2(self):
        # Update the selected signal's name based on the content of the edit textbox
        selected_index = self.select_signal2.currentIndex()
        new_name = self.edit_signal_name2.text()

        if selected_index >= 0 and new_name:
            # Update the name in the signal_names list
            self.signal_names2[selected_index] = new_name

            # Update the name in the select menu
            self.select_signal2.setItemText(selected_index, new_name)

    def update_signal_speed1(self):
        speed_value = self.speed_slider1.value()  # Get the value from the slider
        self.signals_speed1= speed_value  # Update the speed list

    def update_signal_visibility1(self):
        # Update the visibility state for the selected signal
        selected_index = self.select_signal1.currentIndex()

        if selected_index >= 0:
            is_visible = self.visibility_checkbox1.isChecked()  # Get the state of the checkbox
            self.signal_visibility1[selected_index] = is_visible  # Update the visibility list

            # Immediately update the plot to reflect the visibility change
            self.canvas1.clear()
            self.update_animation1()

    def update_signal_speed2(self):
        speed_value = self.speed_slider2.value()  # Get the value from the slider
        # print(f"speed value: {speed_value}")
        self.signals_speed2 = speed_value  # Update the speed list

    def update_signal_visibility2(self):
        # Update the visibility state for the selected signal
        selected_index = self.select_signal2.currentIndex()

        if selected_index >= 0:
            is_visible = self.visibility_checkbox2.isChecked()  # Get the state of the checkbox
            self.signal_visibility2[selected_index] = is_visible  # Update the visibility list

            # Immediately update the plot to reflect the visibility change
            self.canvas2.clear()
            self.update_animation2()

    def move_signal_to_graph2(self):
        # Get the selected signal's index in Graph 1
        selected_index = self.select_signal1.currentIndex()

        if selected_index >= 0:
            # Move the signal's data (time, signal values) to Graph 2's lists
            t = self.t_list1.pop(selected_index)
            signal = self.signal_list1.pop(selected_index)
            self.t_list2.append(t)
            self.signal_list2.append(signal)

            # Move the corresponding settings to Graph 2's lists (name, color, speed, visibility)
            signal_name = self.signal_names1.pop(selected_index)
            signal_color = self.signal_colors1.pop(selected_index)
            signal_visibility = self.signal_visibility1.pop(selected_index)
            current_index = self.current_indices1.pop(selected_index)

            self.signal_names2.append(signal_name)
            self.signal_colors2.append(signal_color)
            self.signal_visibility2.append(signal_visibility)
            self.current_indices2.append(current_index)

            # Add the signal's name to the Graph 2 select menu
            self.select_signal2.addItem(signal_name)

            # Remove the signal from the Graph 1 select menu
            self.select_signal1.removeItem(selected_index)
            self.canvas1.clear()
            self.rewind_signal2()

            # # Immediately update both Graph 1 and Graph 2
            # self.canvas1.clear()
            # self.canvas2.clear()
            # self.update_animation1()  # For Graph 1
            # self.start_animation2()
            # self.update_animation2()  # For Graph 2

        if len(self.signal_list1)==0:
            self.edit_signal_name1.clear()  # Clear the textbox
            self.visibility_checkbox1.setChecked(False)  # Uncheck the checkbox
            self.start_button1.setIcon(QIcon(".venv/images/pause.png"))


    def move_signal_to_graph1(self):
        # Get the selected signal's index in Graph 1
        selected_index = self.select_signal2.currentIndex()

        if selected_index >= 0:
            # Move the signal's data (time, signal values) to Graph 2's lists
            t = self.t_list2.pop(selected_index)
            signal = self.signal_list2.pop(selected_index)
            self.t_list1.append(t)
            self.signal_list1.append(signal)

            # Move the corresponding settings to Graph 2's lists (name, color, speed, visibility)
            signal_name = self.signal_names2.pop(selected_index)
            signal_color = self.signal_colors2.pop(selected_index)
            signal_visibility = self.signal_visibility2.pop(selected_index)
            current_index = self.current_indices2.pop(selected_index)

            self.signal_names1.append(signal_name)
            self.signal_colors1.append(signal_color)
            self.signal_visibility1.append(signal_visibility)
            self.current_indices1.append(current_index)

            # Add the signal's name to the Graph 1 select menu
            self.select_signal1.addItem(signal_name)

            # Remove the signal from the Graph 2 select menu
            self.select_signal2.removeItem(selected_index)

            self.canvas2.clear()
            self.rewind_signal1()
            # # Immediately update both Graph 1 and Graph 2
            # self.canvas1.clear()
            # self.canvas2.clear()
            # self.start_animation1()
            # self.update_animation1()  # For Graph 1
            # self.update_animation2()  # For Graph 2

            # If Graph 2 has no more signals, clear the Edit Name and Visibility Checkbox
            if len(self.signal_list2) == 0:
                self.edit_signal_name2.clear()  # Clear the textbox
                self.visibility_checkbox2.setChecked(False)  # Uncheck the checkbox
                self.start_button2.setIcon(QIcon(".venv/images/pause.png"))



    def link_graphs_function(self):
        if not self.graphs_linked:
            if len(self.signal_list1) != 0 and len(self.signal_list2)!=0:
                # Link the graphs - make both move together
                self.link_graphs_functionality()
                self.link_graphs.setText("Unlink Graphs")
                self.graphs_linked = True
        else:
            # Unlink the graphs - make both move independently
            self.unlink_graphs_functionality()
            self.link_graphs.setText("Link Graphs")
            self.graphs_linked = False

    def link_graphs_functionality(self):
         # Reset the signal indices in both Graph 1 and Graph 2
            self.current_indices1 = [0] * len(self.signal_list1)  # Reset all signals in Graph 1
            self.current_indices2 = [0] * len(self.signal_list2)  # Reset all signals in Graph 2

            # Update both graphs to start from the beginning
            self.canvas1.clear()
            self.canvas2.clear()
            self.update_animation1()
            self.update_animation2()

            # Start both animations
            self.start_animation1()
            self.start_animation2()

            self.link_pause.show()
            self.link_zoom_in.show()
            self.link_zoom_out.show()
            self.link_rewind.show()
            self.start_button1.hide()
            self.zoom_in_button1.hide()
            self.zoom_out_button1.hide()
            self.rewind_button1.hide()
            self.start_button2.hide()
            self.zoom_in_button2.hide()
            self.zoom_out_button2.hide()
            self.rewind_button2.hide()

    def unlink_graphs_functionality(self):
        # Unlink the two graphs by giving them independent timelines
        if hasattr(self, 'timer1') and hasattr(self, 'timer2'):
             # Stop any linked timers if they are running
            self.timer1.stop()
            self.timer2.stop()

            # Re-initialize both animations to run independently
            self.timer1 = QTimer()
            self.timer1.timeout.connect(self.update_animation1)
            self.timer1.start(self.speed_slider1.value())  # Set speed from the slider for graph 1

            self.timer2 = QTimer()
            self.timer2.timeout.connect(self.update_animation2)
            self.timer2.start(self.speed_slider2.value())  # Set speed from the slider for graph 2
            self.link_pause.hide()
            self.link_zoom_in.hide()
            self.link_zoom_out.hide()
            self.link_rewind.hide()
            self.start_button1.show()
            self.zoom_in_button1.show()
            self.zoom_out_button1.show()
            self.rewind_button1.show()
            self.start_button2.show()
            self.zoom_in_button2.show()
            self.zoom_out_button2.show()
            self.rewind_button2.show()

            # print("Graphs are now unlinked and move independently.")
            self.start_button1.setIcon(QIcon(".venv/images/pause.png"))
            self.start_button2.setIcon(QIcon(".venv/images/pause.png"))


    def pause_icon1(self):
        if self.timer1.isActive():
            self.start_button1.setIcon(QIcon(".venv/images/pause.png"))
        else:
            self.start_button1.setIcon(QIcon(".venv/images/start-green.png"))

    def pause_icon2(self):
        if self.timer2.isActive():
            self.start_button2.setIcon(QIcon(".venv/images/pause.png"))
        else:
            self.start_button2.setIcon(QIcon(".venv/images/start-green.png"))

    def pause_signal1(self):
        if hasattr(self, 'timer1') and self.timer1.isActive():
            self.timer1.stop()  # Stop the timer to pause the animation
            print("Signal 1 paused.")
        else:
            # If the timer is not active, start it to resume the animation
            self.timer1.start(250)
            print("Signal 1 resumed.")
        self.pause_icon1()

    def pause_signal2(self):
        if hasattr(self, 'timer2') and self.timer2.isActive():
            self.timer2.stop()  # Stop the timer to pause the animation
            print("Signal 2 paused.")
        else:
            # If the timer is not active, start it to resume the animation
            self.timer2.start(250)
            print("Signal 2 resumed.")    
        self.pause_icon2()

    def pause_linked_signals(self):  
        if hasattr(self, 'timer1') and self.timer1.isActive():
            self.link_pause.setIcon(QIcon(".venv/images/start-green.png"))
            self.timer1.stop()  # Stop the timer to pause the animation
            print("Signal 1 paused.")
            # Retrieve the viewboxes of both graphs
            view1 = self.canvas1.getViewBox()
            view2 = self.canvas2.getViewBox()

            # Define functions to update the view of the other graph
            def update_view2():
                view2.blockSignals(True)  # Temporarily block signals for view2
                view2.setRange(xRange=view1.viewRange()[0], yRange=view1.viewRange()[1], padding=0)
                view2.blockSignals(False)  # Unblock signals after update

            def update_view1():
                view1.blockSignals(True)  # Temporarily block signals for view1
                view1.setRange(xRange=view2.viewRange()[0], yRange=view2.viewRange()[1], padding=0)
                view1.blockSignals(False)  # Unblock signals after update

            # Connect signals so that changes in one graph update the other
            view1.sigRangeChanged.connect(update_view2)
            view2.sigRangeChanged.connect(update_view1)

            # Store these functions if you need to disconnect them when unpausing
            self._update_view1_func = update_view1
            self._update_view2_func = update_view2
        else:
            self.link_pause.setIcon(QIcon(".venv/images/pause.png"))
            # If the timer is not active, start it to resume the animation
            self.timer1.start(250)
            print("Signal 1 resumed.")
                # Disconnect the view linking if no longer needed while animating
            view1 = self.canvas1.getViewBox()
            view2 = self.canvas2.getViewBox()

            # Disconnect range update functions if they were previously stored
            if hasattr(self, "_update_view1_func") and hasattr(self, "_update_view2_func"):
                view1.sigRangeChanged.disconnect(self._update_view2_func)
                view2.sigRangeChanged.disconnect(self._update_view1_func)

        if hasattr(self, 'timer2') and self.timer2.isActive():
            self.timer2.stop()  # Stop the timer to pause the animation
            print("Signal 2 paused.")
        else:
            # If the timer is not active, start it to resume the animation
            self.timer2.start(250)
            print("Signal 2 resumed.")    
             
    def zoom_in_signal1(self):
        # Set manual zoom flag to True
        self.manual_zoom1 = True

        # Get the current view range (X and Y)
        view_range = self.canvas1.viewRange()
        
        # Get the current X and Y ranges
        x_min, x_max = view_range[0]
        y_min, y_max = view_range[1]
        
        # Prevent zooming in too much (when ranges become too small)
        if (x_max - x_min) > 1e-3 and (y_max - y_min) > 1e-3:
            # Reduce the range by 20% for zooming in
            new_x_range = (x_min + 0.1 * (x_max - x_min), x_max - 0.1 * (x_max - x_min))
            new_y_range = (y_min + 0.1 * (y_max - y_min), y_max - 0.1 * (y_max - y_min))
            
            # Set the new X and Y ranges
            self.canvas1.setXRange(new_x_range[0], new_x_range[1])
            self.canvas1.setYRange(new_y_range[0], new_y_range[1])

    def zoom_in_signal2(self):
        # Set manual zoom flag to True
        self.manual_zoom2 = True

        # Get the current view range (X and Y)
        view_range = self.canvas2.viewRange()
        
        # Get the current X and Y ranges
        x_min, x_max = view_range[0]
        y_min, y_max = view_range[1]
        
        # Prevent zooming in too much (when ranges become too small)
        if (x_max - x_min) > 1e-3 and (y_max - y_min) > 1e-3:
            # Reduce the range by 20% for zooming in
            new_x_range = (x_min + 0.1 * (x_max - x_min), x_max - 0.1 * (x_max - x_min))
            new_y_range = (y_min + 0.1 * (y_max - y_min), y_max - 0.1 * (y_max - y_min))
            
            # Set the new X and Y ranges
            self.canvas2.setXRange(new_x_range[0], new_x_range[1])
            self.canvas2.setYRange(new_y_range[0], new_y_range[1])

    def zoom_in_linked_signals(self):
        self.zoom_in_signal1()
        self.zoom_in_signal2()

    def zoom_out_signal1(self):
        # Set manual zoom flag to True to avoid animation interference
        self.manual_zoom1 = True

        # Get the current view range
        view_range = self.canvas1.viewRange()
        visible_x_min, visible_x_max = view_range[0]  # X-axis range (time)
        visible_min_y, visible_max_y = view_range[1]  # Y-axis range (signal values)

        # Initialize min and max Y-values for the visible portion
        visible_min_y, visible_max_y = float('inf'), float('-inf')

        # Loop through the signals and adjust Y-limits based on visible X-range
        for t, signal in zip(self.t_list1, self.signal_list1):
            # Find the indices corresponding to the visible X-range
            visible_indices = np.where((t >= visible_x_min) & (t <= visible_x_max))

            if len(visible_indices[0]) > 0:  # Ensure there are visible points
                visible_min_y = min(visible_min_y, np.min(signal[visible_indices]))
                visible_max_y = max(visible_max_y, np.max(signal[visible_indices]))

        # Set the new Y-range if the values are valid and not at the limit
        if visible_min_y < float('inf') and visible_max_y > float('-inf'):
            self.canvas1.setYRange(
                visible_min_y - 0.1 * abs(visible_min_y),
                visible_max_y + 0.1 * abs(visible_max_y),
                padding=0.1
            )

        # Now handle the X-axis zoom out
        # First, check if Y-axis is already at the signal's full range
        overall_min_signal = min(np.min(signal) for signal in self.signal_list1)
        overall_max_signal = max(np.max(signal) for signal in self.signal_list1)

        # If the Y-axis is already at its full limit, prevent further X-axis zoom out
        if visible_min_y <= overall_min_signal and visible_max_y >= overall_max_signal:
            print("Y-axis is fully zoomed out, X-axis zoom out prevented.")
            return  # Exit the function without zooming out the X-axis

        # If the Y-axis is not at its limit, allow X-axis zoom out
        x_range = visible_x_max - visible_x_min
        new_x_min = visible_x_min - 0.2 * x_range  # Zoom out 20% to the left
        new_x_max = visible_x_max + 0.2 * x_range  # Zoom out 20% to the right

        # Limit X-range to the signal's time bounds
        min_time = np.min(self.t_list1[0])
        max_time = np.max(self.t_list1[0])

        if new_x_min < min_time:
            new_x_min = min_time
        if new_x_max > max_time:
            new_x_max = max_time

        # Apply the new X-range
        self.canvas1.setXRange(new_x_min, new_x_max, padding=0.1)

        print(f"Signal 1 zoomed out with new X-range: ({new_x_min}, {new_x_max})")


    def zoom_out_signal2(self):
        # Set manual zoom flag to True
        self.manual_zoom2 = True

        # Get the current view range
        view_range = self.canvas2.viewRange()
        visible_x_min, visible_x_max = view_range[0]

        # Initialize min and max Y-values for the visible portion
        visible_min_y, visible_max_y = float('inf'), float('-inf')

        # Loop through the signals and adjust Y-limits based on visible X-range
        for t, signal in zip(self.t_list2, self.signal_list2):
            # Find the indices corresponding to the visible X-range
            visible_indices = np.where((t >= visible_x_min) & (t <= visible_x_max))

            if len(visible_indices[0]) > 0:  # Ensure there are visible points
                visible_min_y = min(visible_min_y, np.min(signal[visible_indices]))
                visible_max_y = max(visible_max_y, np.max(signal[visible_indices]))

        # Ensure the visible min and max Y-values are reasonable before setting them
        if visible_min_y < float('inf') and visible_max_y > float('-inf'):
            self.canvas2.setYRange(visible_min_y - 0.1 * abs(visible_min_y), 
                                visible_max_y + 0.1 * abs(visible_max_y), padding=0.1)

        # Perform zoom out on X-axis (time)
        new_x_range = (visible_x_min * 1.2, visible_x_max * 1.2)
        self.canvas2.setXRange(new_x_range[0], new_x_range[1], padding=0.1)

        print("Signal 1 zoomed out with dynamic Y-limits.")

    def zoom_out_linked_signals(self):
        self.zoom_out_signal1()
        self.zoom_out_signal2()
 
    def rewind_signal1(self):
        self.manual_zoom1=False
        self.start_button1.setIcon(QIcon(".venv/images/pause.png"))
        self.canvas1.clear()
        self.current_indices1 = [0] * len(self.signal_list1)  # Reset all signals in Graph 1
        self.start_animation1()
        self.update_animation1()


    def rewind_signal2(self):
        self.manual_zoom12=False
        self.start_button2.setIcon(QIcon(".venv/images/pause.png"))
        self.canvas2.clear()
        self.current_indices2 = [0] * len(self.signal_list2)  # Reset all signals in Graph 1
        self.start_animation2()
        self.update_animation2()   

    def rewind_linked_signals(self):
        self.manual_zoom1=False
        self.manual_zoom12=False
        self.link_rewind.setIcon(QIcon(".venv/images/pause.png"))
        # Reset the signal indices in both Graph 1 and Graph 2
        self.current_indices1 = [0] * len(self.signal_list1)  # Reset all signals in Graph 1
        self.current_indices2 = [0] * len(self.signal_list2)  # Reset all signals in Graph 2

        # Update both graphs to start from the beginning
        self.update_animation1()
        self.update_animation2()

        # Start both animations
        self.start_animation1()
        self.start_animation2()


    def snapshot_graph3(self):
        # Ensure there is a glued signal
        if not hasattr(self, 'glued_signal') or self.glued_signal is None:
            QMessageBox.warning(self, "Error", "No glued signal available to snapshot.")
            return

        # Define a folder for saving snapshots
        snapshots_dir = os.path.join(os.getcwd(), "snapshots")
        os.makedirs(snapshots_dir, exist_ok=True)

        # Automatically generate a unique filename based on the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(snapshots_dir, f"snapshot_{timestamp}.png")

        # Plot and save the snapshot
        figure, ax = plt.subplots()
        ax.plot(self.glued_signal)
        ax.set_title("Glued Signal Snapshot")
        figure.savefig(image_path, format='png')
        plt.close(figure)

        # Calculate and store statistics along with the image path
        snapshot_data = {
            "image_path": image_path,
            "mean": np.mean(self.glued_signal),
            "std": np.std(self.glued_signal),
            "min": np.min(self.glued_signal),
            "max": np.max(self.glued_signal),
            "duration": len(self.glued_signal)
        }
        self.snapshots.append(snapshot_data)  # Add to the list of snapshots

        print(f"Snapshot saved to {image_path}")

    def generate_pdf_report(self):
        if not self.snapshots:
            QMessageBox.warning(self, "Error", "No snapshots available to generate a report.")
            return

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        for snapshot in self.snapshots:
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, "Glued Signal Report", ln=True, align="C")

            # Insert the snapshot image
            pdf.image(snapshot["image_path"], x=10, y=30, w=180)
            pdf.ln(175)  # Move cursor below the image

            # Add statistics below each image
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(40, 10, "Signal Statistics", ln=True)

            pdf.set_font("Arial", '', 12)
            pdf.cell(40, 10, f"Mean: {snapshot['mean']:.2f}", ln=True)
            pdf.cell(40, 10, f"Standard Deviation: {snapshot['std']:.2f}", ln=True)
            pdf.cell(40, 10, f"Min Value: {snapshot['min']}", ln=True)
            pdf.cell(40, 10, f"Max Value: {snapshot['max']}", ln=True)
            pdf.cell(40, 10, f"Duration: {snapshot['duration']} data points", ln=True)

        # Prompt to save the PDF
        pdf_output_path = QFileDialog.getSaveFileName(self, "Save Report", "", "PDF Files (*.pdf)")[0]
        if pdf_output_path:
            pdf.output(pdf_output_path)
            print(f"PDF report saved to {pdf_output_path}")



   
    def open_home_page(self):
        self.stacked_widget.setCurrentWidget(self.main_widget)
        # self.initUi()

    def open_new_page(self):
        self.stacked_widget.setCurrentWidget(self.new_page)
        if not self.second_page_opened:
            self.init_page2()
            self.second_page_opened=True
   
    def init_page2(self):
        new_page_layout=QVBoxLayout()
        polar_graph_layout=QHBoxLayout()
        polar_graph_layout.setSpacing(100)
        polar_controls_layout=QVBoxLayout()
        polar_graph_buttons=QHBoxLayout()
        self.pause_polar=QPushButton()
        self.pause_polar.setIcon(QIcon(".venv/images/pause.png"))
        self.zoom_in_polar=QPushButton()
        self.zoom_in_polar.setIcon(QIcon(".venv/images/zoom-in.png"))
        self.zoom_out_polar=QPushButton()
        self.zoom_out_polar.setIcon(QIcon(".venv/images/zoom-out.png"))
        self.rewind_polar=QPushButton()
        self.rewind_polar.setIcon(QIcon(".venv/images/rewind.png"))
        polar_graph_buttons.addWidget(self.pause_polar)
        polar_graph_buttons.addWidget(self.zoom_in_polar)
        polar_graph_buttons.addWidget(self.zoom_out_polar)
        polar_graph_buttons.addWidget(self.rewind_polar)
        polar_controls_layout.addLayout(polar_graph_buttons)
        self.pause_polar.clicked.connect(self.pause_polar_function)
        self.zoom_in_polar.clicked.connect(self.zoom_in_polar_function)
        self.zoom_out_polar.clicked.connect(self.zoom_out_polar_function)
        self.rewind_polar.clicked.connect(self.rewind_polar_function)

        self.home_page_button=QPushButton("Home page")
        self.home_page_button.clicked.connect(self.open_home_page)
        self.home_page_button.setFixedWidth(150)
        new_page_layout.addWidget(self.home_page_button)
        self.polar_canvas=self.create_polar_canvas()
        polar_graph_layout.addWidget(self.polar_canvas)

        self.select_label_polar=QLabel("Select signal:")
        self.select_signal_polar=QComboBox()
        self.edit_label_polar=QLabel("Edit signal name:")
        self.edit_signal_name_polar=QLineEdit()
        self.visibility_checkbox_polar=QCheckBox("Visibility")
        self.color_button_polar = QPushButton("Select Color")
        self.speed_label_polar = QLabel("Signal speed")
        self.speed_slider_polar = QSlider(Qt.Horizontal)
        self.browse_button_polar = QPushButton("Browse file")
        self.browse_button_polar.setFixedWidth(150)

        polar_select_layout=QHBoxLayout()
        polar_select_layout.addWidget(self.select_label_polar)
        polar_select_layout.addWidget(self.select_signal_polar)

        polar_edit_layout=QHBoxLayout()
        polar_edit_layout.addWidget(self.edit_label_polar)
        polar_edit_layout.addWidget(self.edit_signal_name_polar)

        polar_color_layout=QHBoxLayout()
        polar_color_layout.addWidget(self.visibility_checkbox_polar)
        polar_color_layout.addWidget(self.color_button_polar)
        self.color_button_polar.clicked.connect(self.select_polar_signal_color)

        polar_speed_layout=QHBoxLayout()
        polar_speed_layout.addWidget(self.speed_label_polar)
        polar_speed_layout.addWidget(self.speed_slider_polar)

        polar_controls_layout.addLayout(polar_select_layout)
        polar_controls_layout.addLayout(polar_edit_layout)
        polar_controls_layout.addLayout(polar_color_layout)
        polar_controls_layout.addLayout(polar_speed_layout)
        polar_controls_layout.addWidget(self.browse_button_polar)
        self.angles=[]
        self.densities=[]
        self.browse_button_polar.clicked.connect(self.load_polar_signal)
        polar_graph_layout.addLayout(polar_controls_layout)
        new_page_layout.addLayout(polar_graph_layout)

        self.polar_timer = QTimer()  # Timer for animation
        self.polar_timer.timeout.connect(self.update_polar_animation)  # Connect timer to update method

        self.edit_signal_name_polar.textChanged.connect(self.update_polar_signal_name)
        self.visibility_checkbox_polar.stateChanged.connect(self.toggle_polar_signal_visibility)
        self.speed_slider_polar.valueChanged.connect(self.update_polar_signal_speed)
        self.paused=False

        self.new_page.setLayout(new_page_layout)


    # Creating the non-rectangular graph

    def create_polar_canvas(self):
        # Create a figure for the polar plot
        self.fig, self.ax = plt.subplots(subplot_kw={'projection': 'polar'})
        
        # Plot the loaded polar data, initially with empty data to set up
        self.line, = self.ax.plot([], [], color='r', linewidth=2)  # Initialize an empty line
        
        # Customize the appearance of the polar plot
        self.ax.set_facecolor('#28292b')  # Set background color
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        # Convert figure into a canvas that can be added to the PyQt window
        canvas = FigureCanvas(self.fig)
        
        return canvas

    def load_polar_signal(self):
        # Open a file dialog to select a CSV file
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Polar Signal File", "", "CSV Files (*.csv)", options=options)
        
        if file_path:
            self.add_signal_to_polar_graph(file_path)
            # Plot the signal in the polar graph and start animation
            self.start_polar_animation()

    def add_signal_to_polar_graph(self, file_path):
        # Load the CSV data using pandas
        df = pd.read_csv(file_path)  # Automatically handles BOM
        self.angles = df.iloc[:, 0].to_numpy()  # Angle values (in degrees or radians)
        self.densities = df.iloc[:, 1].to_numpy()  # Signal values

        # Default signal name
        default_name = "polar_signal"
        
        # Add signal to select menu with default name
        self.select_signal_polar.addItem(default_name)
        
        # Set default name in the edit name textbox
        self.edit_signal_name_polar.setText(default_name)
        
        # Set visibility checkbox checked by default
        self.visibility_checkbox_polar.setChecked(True)

    def start_polar_animation(self):
        # Start the polar animation timer
        self.current_frame = 0
        self.polar_timer.start(200)  # Update every 200 ms

    def update_polar_animation(self):
        # Update the current frame index
        self.current_frame += 1
        
        # Reset the frame counter if it exceeds the length of the data
        if self.current_frame >= len(self.angles):
            self.current_frame = 0
        
        # Update the plot data for animation effect (slice up to the current frame)
        self.line.set_data(np.radians(self.angles[:self.current_frame]), self.densities[:self.current_frame])
        
        # Redraw the canvas to display the updated plot
        self.polar_canvas.draw()

    def update_polar_signal_name(self):
        # Get the current name from the textbox
        new_name = self.edit_signal_name_polar.text()
        
        # Update the selected signal's name in the select menu
        selected_index = self.select_signal_polar.currentIndex()
        self.select_signal_polar.setItemText(selected_index, new_name)

    def toggle_polar_signal_visibility(self):
        # Check the state of the checkbox
        if self.visibility_checkbox_polar.isChecked():
            # Make the signal visible
            self.line.set_visible(True)
        else:
            # Hide the signal
            self.line.set_visible(False)
        
        # Redraw the canvas to apply the visibility change
        self.polar_canvas.draw()

    def select_polar_signal_color(self):
        color = QColorDialog.getColor()

        if color.isValid():
            # Convert QColor to Matplotlib's RGB format
            rgb_color = color.name()  # Get the color as a hex string
            # Assuming 'self.line' is the reference to the signal plot line
            self.line.set_color(rgb_color)  # Update the color of the signal
        
            # Redraw the canvas to apply the color change
            self.polar_canvas.draw()

    def update_polar_signal_speed(self):
        # Get the current value from the slider
        slider_value = self.speed_slider_polar.value()

        # Map the slider value to a suitable interval for the timer (e.g., 50-1000 ms)
        # Assuming the slider gives a value between 1 and 100
        new_interval = 2000 // slider_value  # Faster speed with higher slider values

        # Update the timer interval for the animation
        self.polar_timer.setInterval(new_interval)

    def pause_polar_function(self):
        if self.paused:
            # If paused, resume the animation
            self.polar_timer.start()
            self.pause_polar.setIcon(QIcon(".venv/images/pause.png"))
        else:
            # If running, pause the animation
            self.polar_timer.stop()
            self.pause_polar.setIcon(QIcon(".venv/images/start-green.png"))
        
        # Toggle the paused state
        self.paused = not self.paused

    def zoom_in_polar_function(self):
        ax = self.polar_canvas.figure.gca()  # Get the current polar axis
        r_min, r_max = ax.get_ylim()  # Get current radius limits
        ax.set_ylim(r_min * 0.8, r_max * 0.8)  # Zoom in by 20%
        self.polar_canvas.draw()  # Redraw the canvas

    def zoom_out_polar_function(self):
        ax = self.polar_canvas.figure.gca()  # Get the current polar axis
        r_min, r_max = ax.get_ylim()  # Get current radius limits
        ax.set_ylim(r_min * 1.2, r_max * 1.2)  # Zoom out by 20%
        self.polar_canvas.draw()  # Redraw the canvas

    def rewind_polar_function(self):
        self.current_frame = 0  # Reset the frame index
        self.polar_timer.start()  # Restart the animation if it was paused
        self.pause_polar.setIcon(QIcon(".venv/images/pause.png"))

    def setup_driver(self):
        # Set up WebDriver with Chrome in headless mode
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--disable-web-security')

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    def convert_to_float(self,number_str):
        # Remove commas and convert to float
        cleaned_number = number_str.replace(",", "").replace("$", "")
        print(cleaned_number)
        return float(cleaned_number)
    
    def fetch_real_time_signal(self):
        # Set up WebDriver for real-time signal scraping
        self.setup_driver()
        i=-1
        url = 'https://coinmarketcap.com/currencies/ethereum/'
        self.driver.get(url)

        try:
            while self.is_fetching_real_time:
                # Wait for content to load
                time.sleep(1)

                # Get the HTML content
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                # Find the price element and extract data
                # price_element = soup.find('span', class_='sc-65e7f566-0')
                # Find the span element with both the class and data-test attributes to ensure accuracy
                price_element = soup.find('span', class_='sc-65e7f566-0 WXGwg base-text', attrs={'data-test': 'text-cdp-price-display'})

                if price_element:
                    price = price_element.text.strip()  # Get the text and remove extra spaces
                    price = self.convert_to_float(price_element.text.strip())
                    self.real_time_y.append(price)
                    i+=1
                    self.real_time_x.append(i)

                    print(f"BTC/USDT Price: {price}")
                    self.update_animation_real_time()
                else:
                    print("Price element not found.")
        
        except Exception as e:
            print(f"Error fetching real-time signal: {e}")

        finally:
            self.driver.quit()
    
    def start_real_time_signal(self):
        if self.is_fetching_real_time==False:
            self.is_fetching_real_time = True  # Set flag to start fetching
            self.real_signal_button1.setText("Stop real signal")
            # Run the fetch_real_time_signal function in a separate thread
            threading.Thread(target=self.fetch_real_time_signal).start()

            # Start the animation for real-time updates
            self.start_animation_real_time()
        else:
            self.is_fetching_real_time=False
            self.real_signal_button1.setText("Start real signal")
            self.canvas3.clear()

    def start_animation_real_time(self):
        # Start the timer for real-time signal animation
        self.real_signal_timer.start(175)

    def update_animation_real_time(self):
        self.canvas3.clear()  # Clear previous plot

        if self.real_time_x and self.real_time_y:
            # Plot the real-time signal
            pen = pg.mkPen(color='#00ff00', width=2)  # Green for real-time signal
            self.canvas3.plot(self.real_time_x, self.real_time_y, pen=pen)

            # Set the X-axis to show only the latest part of the signal
            if len(self.real_time_x) > self.window_size1:
                start_index = len(self.real_time_x) - self.window_size1
                self.canvas3.setXRange(self.real_time_x[start_index], self.real_time_x[-1], padding=0)
            else:
                self.canvas3.setXRange(0, len(self.real_time_x), padding=0)

            # Set Y-axis to dynamic range of the real-time signal
            min_signal, max_signal = min(self.real_time_y), max(self.real_time_y)
            self.canvas3.setYRange(min_signal - 0.1 * abs(min_signal), max_signal + 0.1 * abs(max_signal), padding=0.1)
        
        # Stop the timer when no real-time data is being fetched
        if not self.is_fetching_real_time:
            self.real_signal_timer.stop()
    
    def open_glue_signals_window(self):
        self.canvas3.clear()
        selected_index1=self.select_signal1.currentIndex()
        selected_index2=self.select_signal2.currentIndex()
        self.signal1=self.signal_list1[selected_index1]
        self.signal2=self.signal_list2[selected_index2]
        self.glue_window = GlueSignalsWindow(self.signal1, self.signal2, parent=self)
        self.glue_window.show()

    def update_glue_window_gap(self):
        gap_value=self.gap_textbox.text()
        GlueSignalsWindow.set_gap(gap_value)


    def plot_glued_signal_with_colors(self, signal1_portion, gap_signal, signal2_portion,glued_signal):
        # Clear the canvas
        self.canvas3.clear()
        selected_index1=self.select_signal1.currentIndex()
        selected_index2=self.select_signal2.currentIndex()
        pen1=self.signal_colors1[selected_index1]
        pen2=self.signal_colors2[selected_index2]
        self.glued_signal=glued_signal

        # Get lengths for x-axis positioning
        len1 = len(signal1_portion)
        len_gap = len(gap_signal)
        len2 = len(signal2_portion)
        total_len=len1+len2+len_gap

        # Generate x-axis values for each part
        x1 = np.arange(len1)
        x_gap = np.arange(len1, len1 + len_gap)
        x2 = np.arange(len1 + len_gap, len1 + len_gap + len2)

        self.canvas3.setXRange(0, total_len)  # Set X range to the full length of the signal
        self.canvas3.enableAutoRange('y')  # Auto-adjust Y range to fit the signal

        # Plot with overlapping points to ensure continuity
        if len1 > 0:
            self.canvas3.plot(x1, signal1_portion, pen=pen1)
        
        if len_gap > 0:
            # Include last point of signal1 and first point of signal2 in gap plotting
            x_gap_extended = np.concatenate([[len1 - 1], x_gap, [len1 + len_gap]])
            gap_extended = np.concatenate([[signal1_portion[-1]], gap_signal, [signal2_portion[0]]])
            self.canvas3.plot(x_gap_extended, gap_extended, pen='r')
        
        if len2 > 0:
            self.canvas3.plot(x2, signal2_portion, pen=pen2)

        print(f"Signal 1: {len1}, Signal 2: {len2}, Gap: {len_gap}")

        # Refresh the canvas to show the updated plot
        # self.canvas3.draw()

app=QApplication(sys.argv)
window=SignalViewer()
window.show()    
sys.exit(app.exec_())
