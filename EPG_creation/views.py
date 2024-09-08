from django.shortcuts import render, redirect
import schedule
import time
from schedule import repeat, every
import xml.etree.ElementTree as ET
from .models import Listing, Listing2
import csv
from datetime import datetime
import os
from django.views import View
from django.http import HttpResponse
from .forms import UploadFileForm
from django.template import loader
from django.contrib.auth import logout
import io
import chardet
import pandas as pd



def index(request):
    template = loader.get_template('EPG_generator.html')
    context = {}
    return HttpResponse(template.render(context, request))

class EPG(View):
    template_name = 'EPG_generator.html'
    form_class = UploadFileForm

                
    def save_epg_file(self, uploaded_file):
          uploaded_file_utf8 = uploaded_file.read().decode('utf-8')
          uploaded_file_stringio = io.StringIO(uploaded_file_utf8)

          reader = csv.DictReader(uploaded_file_stringio)

          next(reader)
             

          for row in reader:
                start_date_str = row['Start Date'] 
                start_time_str = row['Start Time']
                program_title = row['Program Title']
                classification = row['Classification']
                digital_epg_synopsis = row['Digital EPG Synopsis']
                episode_title = row['Episode Title']
                major_program_genre = row['Major Programme Genre']
                sub_genre = row['Sub Genre']
                year_of_production = row['Year of Production']
                if not year_of_production:
                    continue
                actors = row['Actors']
                nominal_length = row['Nominal Length']
                closed_captions = row['Closed Captions']
                premiere_episode = row['Preimere Episode/New Episode']

                
                start_date = datetime.strptime(start_date_str, '%m/%d/%Y')
                start_time = datetime.strptime(start_time_str, '%I:%M %p').time()
                closed_captions_bool  = closed_captions.lower() == 'yes'

                listing_obj = Listing.objects.create(
                    Start_date=start_date,
                    Start_time=start_time,
                    Program_title=program_title,
                    Clasification=classification,
                    Digital_EPG_synopsis=digital_epg_synopsis,
                    Episode_title=episode_title,
                    Major_program_genre=major_program_genre,
                    Sub_genre=sub_genre,
                    Year_of_production=year_of_production,
                    Actors=actors,
                    Nominal_length=nominal_length,
                    Closed_captions=closed_captions_bool,
                    Premiere_episode=premiere_episode,
                )
                listing_obj.save()

    def save_another_epg(self, uploaded_file):

            uploaded_file_utf8 = uploaded_file.read().decode('utf-8')
            uploaded_file_stringio = io.StringIO(uploaded_file_utf8)
            
            reader = csv.DictReader(uploaded_file_stringio)
            
        

            for row in reader:
                print(row)
                date_str = row['DATE']
                time_str = row['TIME']
                name_of_program = row['NAME OF PROGRAM']
                description = row['DESCRIPTION']


                date = datetime.strptime(date_str, '%d.%M.%Y' )
                time = datetime.strptime(time_str, '%H:%M:%S')

                listing2_obj = Listing2.objects.create(
                    Date = date,
                    Time = time,
                    Name_of_program = name_of_program,
                    Description = description
                )
                listing2_obj.save()


    def create_xml(self, listing_obj, filename):
        root = ET.Element("Listings")
        for listing in listing_obj:
              listing_elem = ET.SubElement(root, "listing")
              date_elem = ET.SubElement(listing_elem, "Start_date")
              date_elem.text = listing.Start_date.strftime('%m/%d/%Y')
              time_elem = ET.SubElement(listing_elem, "Start_time")
              time_elem.text = listing.Start_time.strftime('%I:%M %p')
              program_elem = ET.SubElement(listing_elem, "Program_title")
              program_elem.text = listing.Program_title
              classification_elem = ET.SubElement(listing_elem, "Clasification")
              classification_elem.text = listing.Clasification
              digital_epg_synopsis_elem = ET.SubElement(listing_elem, "Digital_EPG_synopsis")
              digital_epg_synopsis_elem.text = listing.Digital_EPG_synopsis
              episode_title_elem = ET.SubElement(listing_elem, "Episode_title")
              episode_title_elem.text = listing.Episode_title
              major_program_genre_elem = ET.SubElement(listing_elem, "Major_program_genre")
              major_program_genre_elem.text = listing.Major_program_genre
              sub_genre_elem = ET.SubElement(listing_elem, "Sub_genre")
              sub_genre_elem.text = listing.Sub_genre
              year_of_production_elem = ET.SubElement(listing_elem, "Year_of_production")
              year_of_production_elem.text = str(listing.Year_of_production)
              actors_elem = ET.SubElement(listing_elem, "Actors")
              actors_elem.text = listing.Actors
              nominal_length_elem = ET.SubElement(listing_elem, "Nominal_length")
              nominal_length_elem.text = str(listing.Nominal_length)
              closed_captions_elem = ET.SubElement(listing_elem, "Closed_captions")
              closed_captions_elem.text = str(listing.Closed_captions)
              premiere_episode_elem = ET.SubElement(listing_elem, "Premiere_episode")
              premiere_episode_elem.text = listing.Premiere_episode
                    

        tree = ET.ElementTree(root)
        output_folder = "C:\\Users\\obero\\.venv\\TV_MEDIA\\EPG_creation\\XML_files"
        filepath = os.path.join(output_folder, filename)
        tree.write(filepath, encoding="utf-8", xml_declaration=True)

    def create_other_xml(self, listing2_obj, filename):
        root = ET.Element("Listings")
        for listing in listing2_obj:
            listing_elem = ET.SubElement(root, "listing")
            date_elem = ET.SubElement(listing_elem, "Date")
            date_elem.text = listing.Date.strftime('%d.%m.%Y')
            time_elem = ET.SubElement(listing_elem, 'Time')
            time_elem.text = listing.Time.strftime('%H:%M:%S')
            name_of_program_elem = ET.SubElement(listing_elem, 'Name_of_program')
            name_of_program_elem.text = listing.Name_of_program
            description_elem = ET.SubElement(listing_elem, 'Description')
            description_elem.text = listing.Description

        tree = ET.ElementTree(root)
        output_folder = "C:\\Users\\obero\\.venv\\TV_MEDIA\\EPG_creation\\smaller_XML_files"
        filepath = os.path.join(output_folder, filename)
        tree.write(filepath, encoding="utf-8", xml_declaration=True)

    def get_number_of_columns(self, uploaded_file):
         
          df = pd.read_csv(uploaded_file)
    
           
          num_columns = len(df.columns)
            
          return num_columns

                    


    def get(self, request):
        return render(request, 'EPG_generator.html', {'form': UploadFileForm()})
    

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
                uploaded_file = request.FILES['file']
                

                custom_filename = request.POST.get('custom_filename')
                self.save_epg_file(uploaded_file)
                listings = Listing.objects.all()
                self.create_xml(listings, custom_filename + ".xml")
                return HttpResponse("File uploaded successfully")
        else:
            return render(request, 'EPG_generator.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
