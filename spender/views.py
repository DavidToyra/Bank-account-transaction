from io import TextIOWrapper
from django.shortcuts import render
import csv
from django.contrib.staticfiles import finders


# Display the table
def monthly_totals3(request, csvfile, filters):
    # Create a dictionary to store the sum of amounts for each month and shop
    monthly_totals = {}
   
    #shop_totals = {item: {} for item in filters} 
    shop_totals = {}
 
   
    # Open the CSV file and read its content
    reader = csv.reader(csvfile, delimiter=';')

    next(reader)  # skip the header row
    # Loop through each row in the CSV file
    for row in reader:
        # Extract the year and month from the "Bokföringsdag" column
        year_month = row[0][:7]

        # Extract the amount from the "Belopp" column and convert it to a float
        amount = float(row[1].replace(',', '.'))

        shop_item = ""
        #Check if the transaction matches any of the filters
        for shop in filters:
            # Turn the strings to same case before comparing
            if shop.lower() in row[5].lower():
                shop_item = shop
                 # Add the amount to the monthly total for this year and month
                if year_month in monthly_totals:
                    monthly_totals[year_month] += amount
                    shop_totals[year_month]["Total"] += amount
                else:
                    monthly_totals[year_month] = amount
                    shop_totals[year_month] = {}
                    shop_totals[year_month]["Total"] = amount

            # Add the amount to the shop total for this year, month and shop
                if year_month in shop_totals:
                    if shop_item in shop_totals[year_month]:
                        shop_totals[year_month][shop_item] += amount
                    else:
                        shop_totals[year_month][shop_item] = amount
                else:
                    shop_totals[year_month] = {}
                    shop_totals[year_month][shop_item] = amount
    print(shop_totals)

    shop_totals_sorted = {}
    filters.insert(0, "Total")
    for year_month, shops in shop_totals.items():
        # Use a lambda function to return the index of each shop in the shop_order list
        # This will be used as the key function for sorting the dictionary
        key_func = lambda x: filters.index(x[0])
        shops_sorted = sorted(shops.items(), key=key_func)
        shop_totals_sorted[year_month] = dict(shops_sorted)

    filters.pop(0)

    total_string = " ".join(filters)
    # Render the template with the monthly and shop totals
    return render(request, 'index2.html', {
        'monthly_totals': monthly_totals,
        'shop_totals': shop_totals_sorted,
        'filters': filters,
        "fullstring": total_string
    })




def upload_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:

        # Read the uploaded CSV file
        csv_file = request.FILES['csv_file']
        csv_data = TextIOWrapper(csv_file.file, encoding='utf-8')
        filter_input = request.POST.get('text', '')
        filters = [t.strip() for t in filter_input.split(',') if t.strip()]
        return monthly_totals3(request, csv_data, filters)
    else:
        return render(request, 'upload_csv.html')




