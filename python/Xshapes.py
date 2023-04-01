
# orangered #FF4500, slategray #708090, lime green #32cd32, firebrick #B22222, aqua #00FFFF, navy #000080
# spring green #00ff7f
# there is no way to change label color for individual nodes
# font_color is set for network
# WARNING edge color is same as "from" node color
dictNodeColors = {
    'unsafeDrug': 'orangered', 
    'safeDrug': 'aqua', 
    'class': 'silver',
    'classTransparent': 'white',
    'testThisDrug': 'navy',
    'digestCode': 'orangered'
}
dictFoodDigestActionColors = {
    'Avoid': 'red',
    'Require': 'blue',
    'Safe': '#00ff7f'
}
#
# shapes with labels inside:
#   ellipse, circle, database, box, text
# size is used for shapes that do NOT have label inside:
#   : image, circularImage, diamond, dot, star, triangle, triangleDown, square and icon
#
dictNodeShapes = {
    'unsafeDrug': 'triangle',
    'safeDrug': 'diamond',
    'testThisDrug': 'star',
    'class': 'box',
    'classDrug1': 'diamond',
    'classDrug2': 'circle'
}
dictNodeImages = {
    'testThisDrug': 'images/star-blue-64.png',
    'testThisDrugSafe':'images/star-green-64.png',
    'testThisDrugUnsafe': 'images/star-red-64.png',
    'safeDrug': 'images/star-green-64.png',
    'unsafeDrug': 'images/star-red-64.png'
}
dictFoodNodeShapes = {
    'foodDigestCode': 'box',    
    'Avoid': 'circle',
    'Require': 'circle',
    'Safe': 'circle'
}
#
# image icons
#
dictFoodDigestActionImages = {
    'Avoid': 'images/avoid-64.png',
    'Require': 'images/require-64.png',
    'Safe': 'images/safe-64.png'
}
dictFoodDigestGroupImages = {
    'Alcohol': 'images/no-alcohol-64.png',
    'Antacids': 'images/antacid-64.png',
    'Caffeine': 'images/caffeine-64.png',
    'Fiber': 'images/no-celery-64.png',
    'Fluids': 'images/fluids-64.png',
    'Foods': 'images/foods-64.png',
    'Grapefruit': 'images/no-grapefruit-64.png',
    'Herbs': 'images/herbs-64.png',
    'Meals': 'images/meals-64.png',
    'Other': 'images/other-64.png',
    'St. John\'s Wort': 'images/no-st-johns-wort-64.png',
    'Supplements': 'images/supplement-64.png',
    'Vitamins': 'images/vitamins-64.png',
}
#
dictNodeSizes = {
    'sizeDefault': 1,
    'sizeOther': 2
}
dictEdgeColors = {
    'colorDefault': 'blue'
}
