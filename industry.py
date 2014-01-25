from app import app
from db import get_all, get_one

class Industry():
    def __init__(self, names=False, category=-1):
        # This query gets inventable items. If category is -1 (default), all inventable items are retrieved. Otherwise, only the requested category is returned. Expected categories: 6, 7, 8, 18, 22.
        if category == -1:
            self.inventable_items = get_all(g_inventable_all['sql'], ())
        else:
            self.inventable_items = get_all(g_inventable_category['sql'], (category))

        self.items = dict()
        self.names = names

    # Retrieve the bill of materials on a perfect blueprint. This will have both sets of items:
    # affected and unaffected by ME waste. The column 'waste' identifies this.
    def perfect_materials(self, item):
        typeid = item['typeID']
        item['perfectMaterials'] = dict()
        materials = get_all(g_perfect_materials['sql'], (typeid, typeid, typeid))

        for material in materials:
            if material[g_perfect_materials['quantity']] > 0:
                typeid = material[g_perfect_materials['typeID']]
                item['perfectMaterials'][typeid] = {
                    'quantity': float(material[g_perfect_materials['quantity']]),
                    'dmg': float(material[g_perfect_materials['dmg']]),
                    'waste': float(material[g_perfect_materials['waste']]),
                }

                if self.names:
                    item['perfectMaterials'][typeid]['name'] = material[g_perfect_materials['name']]

    # Retrieve item blueprint information.
    def item_info(self, typeid):
        try:
            item_row = get_one(g_item['sql'], (typeid))
            self.items[typeid] = {
                'typeName': item_row[g_item['typeName']],
                'typeID': item_row[g_item['typeID']],
                'productionTime': item_row[g_item['productionTime']],
                'productivityModifier': item_row[g_item['productivityModifier']],
                'wasteFactor': item_row[g_item['wasteFactor']],
                'maxProductionLimit': item_row[g_item['maxProductionLimit']],
                'chance': item_row[g_item['chance']],
            }

            return True
        except LookupError:
            # Ignore this error. Can't find the blueprint for this item in the db.
            app.logger.warning('Unable to locate blueprint for item <%d>' % (typeid))
            return False

    # Retrieve the decryptor category.
    def decryptor_category(self, typeid):
        row = get_one(g_decryptor_category['sql'], (typeid))
        self.items[typeid]['decryptor_category'] = row[g_decryptor_category['valueInt']]

    # Retrieve the data cores. They are stored in an array as there is always two of them.
    def datacores(self, item):
        typeid = item['typeID']
        item['datacores'] = []
        datacores = get_all(g_datacores['sql'], (typeid))

        for datacore in datacores:
            dc = {
                'typeID': datacore[g_datacores['typeID']],
                'quantity': datacore[g_datacores['quantity']]
            }

            if self.names:
                dc['typeName'] = datacore[g_datacores['typeName']]

            item['datacores'].append(dc);

    def fetch(self):
        for item in self.inventable_items:
            typeid = item[g_inventable_all['typeID']]
            if self.item_info(typeid):
                self.decryptor_category(typeid)

                if typeid in self.items:
                    self.perfect_materials(self.items[typeid])
                    self.datacores(self.items[typeid])

        return self.items

# Query for item information. Expects one typeid.
g_item = {
    'sql': '''
select invTypes.typeID, typeName, productionTime, productivityModifier, wasteFactor, maxProductionLimit, chance
from invTypes, invBlueprintTypes, inventionChance
where invTypes.typeID = invBlueprintTypes.productTypeID
    and inventionChance.typeID = invTypes.typeID
    and invTypes.typeID = %s''',
    'typeID': 0,
    'typeName': 1,
    'productionTime': 2,
    'productivityModifier': 3,
    'wasteFactor': 4,
    'maxProductionLimit': 5,
    'chance': 6
}

# This query retrieves the perfect bill of materials. It requires the typeid three times.
g_perfect_materials = {
    'sql': '''
select typeid,name,greatest(0,sum(quantity)) quantity, 1 dmg, true waste from (
    select invTypes.typeid typeid,invTypes.typeName name,quantity
    from invTypes,invTypeMaterials
    where invTypeMaterials.materialTypeID=invTypes.typeID
        and invTypeMaterials.TypeID=%s
union
    select invTypes.typeid typeid,invTypes.typeName name, invTypeMaterials.quantity*r.quantity*-1 quantity
    from invTypes,invTypeMaterials,ramTypeRequirements r,invBlueprintTypes bt
    where invTypeMaterials.materialTypeID=invTypes.typeID
        and invTypeMaterials.TypeID =r.requiredTypeID
        and r.typeID = bt.blueprintTypeID
        and r.activityID = 1 and bt.productTypeID=%s and r.recycle=1
) t group by typeid, name
union
select t.typeID typeid, t.typeName name, r.quantity quantity, r.damagePerJob dmg, false waste
from ramTypeRequirements r, invTypes t, invBlueprintTypes bt, invGroups g
where r.requiredTypeID = t.typeID
    and r.typeID = bt.blueprintTypeID
    and r.activityID = 1
    and bt.productTypeID=%s
    and g.categoryID != 16
    and t.groupID = g.groupID''',
    'typeID': 0,
    'name': 1,
    'quantity': 2,
    'dmg': 3,
    'waste': 4
}

# Query to retrieve all inventable items.
g_inventable_all = {
    'sql': '''
select invTypes.typeID, invTypes.typeName, invGroups.categoryID
from invTypes, invMetaTypes, invGroups
where invTypes.typeID=invMetaTypes.typeID
    and invMetaTypes.metaGroupId=2
    and invGroups.groupID=invTypes.groupID
    and invTypes.published=1
order by invGroups.categoryID, invTypes.typeName''',
    'typeID': 0,
    'typeName': 1,
    'categoryID': 2
}

# Query to retrieve inventable items in a given category. Expects one category ID.
g_inventable_category = {
    'sql': '''
select invTypes.typeID, invTypes.typeName, invGroups.categoryID
from invTypes, invMetaTypes, invGroups
where invTypes.typeID=invMetaTypes.typeID
    and invMetaTypes.metaGroupId=2
    and invGroups.groupID=invTypes.groupID
    and invTypes.published=1
    and invGroups.categoryID=%s
order by invGroups.categoryID, invTypes.typeName''',
    'typeID': 0,
    'typeName': 1,
    'categoryID': 2
}

# Query to retrieve the decryptor category. Expects one inventable item ID.
g_decryptor_category = {
    'sql': '''
select valueInt
from dgmTypeAttributes
where attributeID=1115 and typeID=
(select it2.typeid
from invTypes,invGroups,invMetaTypes,ramTypeRequirements,invBlueprintTypes,invTypes it2
where invTypes.typeid=invMetaTypes.typeid and invMetaTypes.metaGroupId=2 and invGroups.groupid=invTypes.groupid and invBlueprintTypes.blueprintTypeID=ramTypeRequirements.typeid and invBlueprintTypes.productTypeID=invMetaTypes.parenttypeid and it2.typeid=requiredTypeID and activityID=8 and it2.groupID=716 and invTypes.typeid=%s)''',
    'valueInt': 0
}

# Query to retrieve the datacores required. Expects on inventable item ID.
g_datacores = {
    'sql': '''
select it2.typeid,it2.typename,quantity
from invTypes,invGroups,invMetaTypes,ramTypeRequirements,invBlueprintTypes,invTypes it2
where invTypes.typeid=invMetaTypes.typeid and invMetaTypes.metaGroupId=2 and invGroups.groupid=invTypes.groupid and invBlueprintTypes.blueprintTypeID=ramTypeRequirements.typeid and invBlueprintTypes.productTypeID=invMetaTypes.parenttypeid and it2.typeid=requiredTypeID and activityID=8 and it2.groupID!=716 and invTypes.typeid=%s''',
    'typeID': 0,
    'typeName': 1,
    'quantity': 2
}
