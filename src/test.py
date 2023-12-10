# ques = '''Generate an email campaign calendar for {} 
#     with a focus on {} 
#     around {}, 
#     considering {} and {}, targeted at {}.'''.format("barcelnoa", "ok", "ok", "ok", "ok", "ok")

# print(ques)


prompt = '''

"Please Rephrase this given text, "Generate weekly calendar campaigns, for the shopify store
                {shop_categories} with a focus on {content_concept_n_narrative}
                around {seasionality}, considering {key_e_commerce_dates} and {industry_specific_key_days},
                targeted at {shop_locations},  
                I want you to return a table with campaign ideas, reasoning, targeted audiences."


'''


prompt = '''
Craft a three-month weekly promotional schedule for The Body Shop's Shopify platform, centered on skincare, haircare, and body products for winter. The output should be a table comprising campaign concepts, justifications, and specific demographics for the online storefront's various categories.
'''

# print(len(prompt))




prompt = '''

Certainly! Below are HTML tables to suggest at least one product for each campaign for a weekly calendar spread over the next three months. Each campaign represents a week and the chosen products align with potential winter-themed promotions for skin, hair, and body care.

**Week 1: Skin Hydration Focus**
```html
<table border="1">
  <tr>
    <th>Week</th>
    <th>Product Suggestion</th>
    <th>Description</th>
    <th>Reason for Selection</th>
  </tr>
  <tr>
    <td>Week 1</td>
    <td>Truffle Mini Popcorn</td>
    <td>Rich in umami, truffles can offer indulgence that's great for a pamper evening.</td>
    <td>Winter is harsh on skin, including this luxury snack in self-care routines can enhance the experience.</td>
  </tr>
</table>
```

**Week 2: Hair Nourishment Week**
```html
<table border="1">
  <tr>
    <th>Week</th>
    <th>Product Suggestion</th>
    <th>Description</th>
    <th>Reason for Selection</th>
  </tr>
  <tr>
    <td>Week 2</td>
    <td>Sea Salt Mini Popcorn</td>
    <td>Light and crispy, seasoned with just enough sea salt for a balanced taste.</td>
    <td>Sea salt is known for its minerals beneficial for skin and hair, making this a thematic fit.</td>
  </tr>
</table>
```

**Week 3: Soothing Body Care**
```html
<table border="1">
  <tr>
    <th>Week</th>
    <th>Product Suggestion</th>
    <th>Description</th>
    <th>Reason for Selection</th>
  </tr>
  <tr>
    <td>Week 3</td>
    <td>Cheddar Cheese Balls</td>
    <td>Cheese contains proteins that support body repair. These balls are also organic and non-GMO.</td>
    <td>Cheese-based snacks can be associated with comfort, hence aligning with body care in the winter season.</td>
  </tr>
</table>
```

Repeat this format to continue the product campaign suggestions for the remaining weeks. Ensure each selection has a connection to the theme of the week, and remember to adjust the reasons for selection to reflect how the product supports or aligns with the campaign's focus.

Please tailor the exact weeks, product selections, descriptions, and reasoning for selection to your specific product line and marketing goals.




'''



# print(len(prompt))

print(any([1,False,False]))
print(all([1,False,False]))
