from flask import Flask, request, jsonify, send_file
import pandas as pd

app = Flask(__name__)

# Endpoint to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_files():
    group_info = request.files['group_info']
    hostel_info = request.files['hostel_info']
    
    # Save the uploaded files
    group_info.save('group_info.csv')
    hostel_info.save('hostel_info.csv')
    
    # Process the files and allocate rooms
    allocation_details = process_files('group_info.csv', 'hostel_info.csv')
    
    # Generate and save CSV output
    allocation_details.to_csv('allocation_details.csv', index=False)
    
    # Return JSON response or file download link
    return send_file('allocation_details.csv', as_attachment=True)

def process_files(group_filename, hostel_filename):
    # Read CSV files
    group_data = pd.read_csv(group_filename)
    hostel_data = pd.read_csv(hostel_filename)
    
    # Perform room allocation logic (pseudo code)
    allocation_details = allocate_rooms(group_data, hostel_data)
    
    return allocation_details

def allocate_rooms(group_data, hostel_data):
    # Initialize allocation details
    allocation_details = []
    
    # Process each group
    for index, group_row in group_data.iterrows():
        group_id = group_row['Group ID']
        group_members = group_row['Members']
        group_gender = group_row['Gender']
        
        # Filter hostels by gender
        filtered_hostels = hostel_data[hostel_data['Gender'] == group_gender]
        
        # Sort hostels by capacity descending
        sorted_hostels = filtered_hostels.sort_values(by='Capacity', ascending=False)
        
        allocated = False
        
        # Try to allocate in sorted hostels
        for index, hostel_row in sorted_hostels.iterrows():
            if allocated:
                break
            
            hostel_name = hostel_row['Hostel Name']
            room_number = hostel_row['Room Number']
            room_capacity = hostel_row['Capacity']
            
            # Check if room can accommodate the group
            if room_capacity >= group_members:
                # Allocate members to this room
                allocation_details.append({
                    'Group ID': group_id,
                    'Hostel Name': hostel_name,
                    'Room Number': room_number,
                    'Members Allocated': group_members
                })
                allocated = True
        
        # If not allocated, handle this case (optional)
        if not allocated:
            allocation_details.append({
                'Group ID': group_id,
                'Hostel Name': 'Not Allocated',
                'Room Number': 'N/A',
                'Members Allocated': group_members
            })
    
    # Convert to DataFrame
    allocation_df = pd.DataFrame(allocation_details)
    
    return allocation_df

if __name__ == '__main__':
    app.run(debug=True)
