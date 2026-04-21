# TO RUN THIS APPLICATION 
 follow the steps

## 1.open HRMS into into vs code
## 2. Press ctrl + j (terminal will open)

#  Paste the below line as it is
## waitress-serve --host=127.0.0.1 --port=4000 app:app  and Press enter

SELECT p.army_number
FROM personnel p
LEFT JOIN weight_info w 
    ON p.army_number = w.army_number
WHERE w.army_number IS NULL;



use copy_hrms;
insert into hrms.weight_info 
(army_number,`rank`,name,actual_weight,height,company,age)
select p.army_number,
p.`rank`,
p.name,
p.actual_weight,
p.height,
p.company,
timestampdiff(YEAR,p.date_of_birth,curdate()) as age
from personnel p where p.army_number = ''
















@leave_bp.route("/download_certificate/<army_number>")
def download_leave_certificate(army_number):
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        print("in this download route")
        # Fetch main leave data with ALL related information
        cursor.execute("""
            SELECT
                l.id as leave_id,
                l.leave_type,
                l.leave_days,
                l.from_date,
                l.to_date,
                l.prefix_date,
                l.suffix_date,
                l.prefix_days,
                l.suffix_days,
                l.created_at as applied_on,
                l.updated_at as issue_date,
                l.leave_reason,
                l.remarks,
                l.request_status,
                p.name,
                p.army_number,
                p.rank,
                p.company,
                p.section,
                p.trade,
                p.i_card_no,
                p.home_house_no,
                p.home_village,
                p.home_phone,
                p.home_to,
                p.home_po,
                p.home_ps,
                p.home_teh,
                p.home_nrs,
                p.home_nmh,
                p.home_district,
                p.home_state,
                m.number AS mobile_number,
                -- Transport information
                lt.transport_id as transport_id,
                lt.onward_mode,
                lt.onward_air_type,
                lt.onward_train_type,
                lt.return_mode,
                lt.return_air_type,
                lt.return_train_type,
                -- Address information
                la.same_as_permanent,
                la.address_line1,
                la.address_line2,
                la.city,
                la.state,
                la.pincode,
                la.mobile as leave_mobile,
                la.alternate_contact
            FROM leave_status_info l
            JOIN personnel p ON p.army_number = l.army_number
            LEFT JOIN mobile_phones m ON m.army_number = l.army_number
            LEFT JOIN leave_transport lt ON lt.leave_request_id = l.id
            LEFT JOIN leave_address la ON la.leave_request_id = l.id
            WHERE l.army_number = %s
              AND l.request_status = 'Approved'
            ORDER BY l.created_at DESC
            LIMIT 1
        """, (army_number,))
        
        data = cursor.fetchone()
        if not data:
            return "No approved leave certificate found for this user.", 404
        
        # ====================== HANDLE COMBINED LEAVE ======================
        leave_type_display = data['leave_type']
        leave_details_list = []
        
        if data['leave_type'] and '+' in data['leave_type']:
            cursor.execute("""
                SELECT leave_type, leave_days, from_date, to_date
                FROM multi_leave_table
                WHERE leave_request_id = %s
                ORDER BY id ASC
            """, (data['leave_id'],))
            multi_leaves = cursor.fetchall()
            
            if multi_leaves:
                formatted_parts = []
                for item in multi_leaves:
                    lt = item['leave_type']
                    days = item['leave_days']
                    formatted_parts.append(f"{lt}({days})")
                    
                    leave_details_list.append({
                        "type": lt,
                        "days": days,
                        "from_date": item['from_date'].strftime('%d-%m-%Y') if item['from_date'] else None,
                        "to_date": item['to_date'].strftime('%d-%m-%Y') if item['to_date'] else None
                    })
                leave_type_display = " + ".join(formatted_parts)
        
        # ====================== FETCH JOURNEY LEGS ======================
        onward_legs = []
        return_legs = []
        
        if data.get('transport_id'):
            cursor.execute("""
                SELECT journey_type, leg_order, from_station, to_station
                FROM leave_journey_legs
                WHERE transport_id = %s
                ORDER BY journey_type, leg_order
            """, (data['transport_id'],))
            
            legs = cursor.fetchall()
            for leg in legs:
                if leg['journey_type'] == 'onward':
                    onward_legs.append({
                        "order": leg['leg_order'],
                        "from": leg['from_station'],
                        "to": leg['to_station']
                    })
                else:
                    return_legs.append({
                        "order": leg['leg_order'],
                        "from": leg['from_station'],
                        "to": leg['to_station']
                    })
        
        # ====================== HANDLE ADDRESS (with permanent address fallback) ======================
        address_during_leave = {}
        
        if data.get('same_as_permanent') == 1 or data.get('same_as_permanent') ==True:
            # Build address from personnel table
            address_parts = []
            print("fixed in the database")
            if data.get('home_house_no'):
                address_parts.append(data['home_house_no'])
            if data.get('home_village'):
                address_parts.append(data['home_village'])
            if data.get('home_to'):
                address_parts.append(data['home_to'])
            if data.get('home_po'):
                address_parts.append(f"PO: {data['home_po']}")
            if data.get('home_ps'):
                address_parts.append(f"PS: {data['home_ps']}")
            if data.get('home_teh'):
                address_parts.append(f"Teh: {data['home_teh']}")
            if data.get('home_district'):
                address_parts.append(f"Dist: {data['home_district']}")
            if data.get('home_state'):
                address_parts.append(data['home_state'])
            if data.get('home_nrs'):
                address_parts.append(f"NRS: {data['home_nrs']}")
            if data.get('home_nmh'):
                address_parts.append(f"NMH: {data['home_nmh']}")
            
            address_during_leave = {
                "full_address": ", ".join(filter(None, address_parts)),
                "is_permanent": True,
                "address_line1": data.get('home_house_no', ''),
                "address_line2": data.get('home_village', ''),
                "city": data.get('home_teh', ''),
                "state": data.get('home_state', ''),
                "pincode": '',  # Not available in personnel table
                "mobile": data.get('leave_mobile') or data.get('mobile_number', 'N/A'),
                "alternate_contact": data.get('alternate_contact', 'N/A')
            }
        else:
            # Use the address provided during leave application
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            address_parts = []
            if data.get('address_line1'):
                address_parts.append(data['address_line1'])
            if data.get('address_line2'):
                address_parts.append(data['address_line2'])
            if data.get('city'):
                address_parts.append(data['city'])
            if data.get('state'):
                address_parts.append(data['state'])
            if data.get('pincode'):
                address_parts.append(f"PIN: {data['pincode']}")
            
            address_during_leave = {
                "full_address": ", ".join(filter(None, address_parts)) or "Address not provided",
                "is_permanent": False,
                "address_line1": data.get('address_line1', ''),
                "address_line2": data.get('address_line2', ''),
                "city": data.get('city', ''),
                "state": data.get('state', ''),
                "pincode": data.get('pincode', ''),
                "mobile": data.get('leave_mobile') or data.get('mobile_number', 'N/A'),
                "alternate_contact": data.get('alternate_contact', 'N/A')
            }
        
        # ====================== FORMAT TRANSPORT INFORMATION ======================
        transport_info = {
            "onward": {
                "mode": data.get('onward_mode', 'Not Specified'),
                "type": None,
                "legs": onward_legs,
                "full_route": " → ".join([f"{leg['from']} to {leg['to']}" for leg in onward_legs]) if onward_legs else "Not specified"
            },
            "return": {
                "mode": data.get('return_mode', 'Not Specified'),
                "type": None,
                "legs": return_legs,
                "full_route": " → ".join([f"{leg['from']} to {leg['to']}" for leg in return_legs]) if return_legs else "Not specified"
            }
        }
        
        # Add specific type details based on mode
        if data.get('onward_mode') == 'Air' and data.get('onward_air_type'):
            transport_info["onward"]["type"] = data['onward_air_type']
        elif data.get('onward_mode') == 'Train' and data.get('onward_train_type'):
            transport_info["onward"]["type"] = data['onward_train_type']
        
        if data.get('return_mode') == 'Air' and data.get('return_air_type'):
            transport_info["return"]["type"] = data['return_air_type']
        elif data.get('return_mode') == 'Train' and data.get('return_train_type'):
            transport_info["return"]["type"] = data['return_train_type']
        
        # ====================== CALCULATE ACTUAL LEAVE DAYS ======================
        actual_leave_days = data.get('leave_days', 0)

        # Subtract prefix and suffix days to get actual core leave days
        if data.get('prefix_days'):
            actual_leave_days -= int(data.get('prefix_days', 0))
        if data.get('suffix_days'):
            actual_leave_days -= int(data.get('suffix_days', 0))

        # Ensure it doesn't go negative
        actual_leave_days = max(actual_leave_days, 0)

        # ====================== FORMAT PREFIX & SUFFIX ======================
        prefix_days = int(data.get('prefix_days', 0))
        suffix_days = int(data.get('suffix_days', 0))

        prefix_details = "NIL"
        if prefix_days > 0 and data.get('prefix_date'):
            prefix_details = f"{prefix_days} day(s) w.e.f. {data['prefix_date'].strftime('%d-%m-%Y')}"

        suffix_details = "NIL"
        if suffix_days > 0 and data.get('suffix_date'):
            suffix_details = f"{suffix_days} day(s) w.e.f. {data['suffix_date'].strftime('%d-%m-%Y')}"

        # ====================== PREPARE CERTIFICATE DATA ======================
        current_year = datetime.now().year
        cert_no = f"LEAVE/{current_year}/{data['leave_id']}"

        applicant = {
            "name": data['name'],
            "rank": data['rank'],
            "army_number": data['army_number'],
            "company_name": data['company'],
            "section_name": data['section'] if data['section'] else "HQ",
            "trade": data.get('trade', 'N/A'),
            "contact": data.get('mobile_number', 'N/A'),
            "i_card_no": data.get('i_card_no', 'N/A')
        }

        leave_info = {
            "certificate_number": cert_no,
            "leave_type": leave_type_display,
            "start_date": data['from_date'],
            "end_date": data['to_date'],
            "total_days": data['leave_days'],           
            "actual_leave_days": actual_leave_days,     
            "prefix_days": prefix_days,                 
            "suffix_days": suffix_days,                 
            "prefix_details": prefix_details,           
            "suffix_details": suffix_details,           
            "issue_date": data['issue_date'] if data['issue_date'] else datetime.now(),
            "applied_on": data['applied_on'],
            "leave_reason": data.get('leave_reason', 'Not specified'),
            "remarks": data.get('remarks', 'N/A'),
            "address_during_leave": address_during_leave,
            "transport": transport_info,
            "reporting_date": (data['suffix_date'] if data['suffix_date'] else data['to_date']).strftime('%d-%m-%Y') 
                              if (data.get('suffix_date') or data.get('to_date')) else 'Not specified',
            "leave_details": leave_details_list,
            "request_status": data['request_status']
        }
        
        print(f"Certificate generated for {army_number} with ID: {data['leave_id']}")
        print(leave_info)

        # ====================== FIX LOGO PATHS FOR PDF (pisa/xhtml2pdf) ======================
        import os
        from flask import current_app

        # Build absolute file paths
        static_dir = os.path.join(current_app.root_path, 'static')
        chinar_logo_path = os.path.abspath(os.path.join(static_dir, 'image_for_login_page', 'chinar.jpg'))
        rt_logo_path     = os.path.abspath(os.path.join(static_dir, 'image_for_login_page', 'rt.jpg'))
        

        # Print for debugging (remove after testing)
        print("Chinar logo path:", chinar_logo_path)
        print("RT logo path:", rt_logo_path)
        
        print("Chinar exists:", os.path.exists(chinar_logo_path))
        print("RT exists:", os.path.exists(rt_logo_path))
        

        # Render template with logo paths
        html = render_template(
            "certificate.html", 
            applicant=applicant, 
            leave=leave_info,
            chinar_logo_path=chinar_logo_path,   # absolute path
            rt_logo_path=rt_logo_path       # absolute path
            
        )
        
        # Generate PDF
        pdf_buffer = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)
        
        if pisa_status.err:
            return "Error generating PDF", 500
        
        pdf_buffer.seek(0)
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f"Leave_Certificate_{army_number}_{data['leave_id']}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print(f"Error generating certificate: {e}")
        import traceback
        traceback.print_exc()
        return str(e), 500
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()




select p.army_number from personnel p where not exists (select 1 from weight_info w where w.army_number = p.army_number)


## this below is for copying all daata from personnel to weight_info for fixingin mismatch
insert into hrms.weight_info 
(army_number,`rank`,name,actual_weight,height,company,age)
select p.army_number,
p.`rank`,
p.name,
p.weight,
p.height,
p.company,
timestampdiff(YEAR,p.date_of_birth,curdate()) as age
from hrms.personnel p where not exists (SELECT 1 FROM hrms.weight_info w where w.army_number = p.army_number);






