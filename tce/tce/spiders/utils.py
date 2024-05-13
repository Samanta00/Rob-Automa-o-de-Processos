def parse_date(date_string):

    # Remova os espaços em branco extras e divida a data
    date_parts = date_string.strip().split('/')
    
    # Formato convertido para data DD-MM-YYYY


    formatted_date = f"{date_parts[0]}-{date_parts[1]}-{date_parts[2]}"
    
    return formatted_date
