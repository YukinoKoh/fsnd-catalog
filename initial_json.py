category_json = json.loads("""{
  "all_categories": [
    {
      "created_date": null,
      "id": 29,
      "name": "Books",
      "no_of_visits": 1
    },
    {
      "created_date": null,
      "id": 21,
      "name": "Camping",
      "no_of_visits": 7
    },
    {
      "created_date": null,
      "id": 20,
      "name": "Kitchenware",
      "no_of_visits": 1
    },
    {
      "created_date": null,
      "id": 32,
      "name": "Laptops",
      "no_of_visits": 10
    },

    {
      "created_date": null,
      "id": 31,
      "name": "Susan's Moving Items",
      "no_of_visits": 8
    }
  ]
}""")

for e in category_json['all_categories']:
  category_input = Category(
    name=str(e['name']), 
    id=str(e['id']), 
    no_of_visits=0, 
    user_id=1
    )
  session.add(category_input)
  session.commit()