from app import app
from db import get_all, get_one

class Industry():
    def __init__(self, names=False, category=-1, rigs=True, detail=-1):
        # This query gets inventable items. If category is -1 (default), all inventable items are retrieved. Otherwise, only the requested category is returned. Expected categories: 6, 7, 8, 18, 22.
        # If detail is set it must be an itemid and that will be all the information that is returned.
        self.t1bpo = False

        if detail != -1:
            self.inventable_items = [[detail]]
            self.t1bpo = True
        elif category != -1:
            self.inventable_items = get_all(g_inventable_category['sql'], (category))
        elif rigs == False:
            self.inventable_items = get_all(g_inventable_no_rigs['sql'], ())
        else:
            self.inventable_items = get_all(g_inventable_all['sql'], ())

        self.items = dict()
        self.names = names

    # Retrieve the bill of materials on a perfect blueprint. This will have both sets of items:
    # affected and unaffected by ME waste. The column 'waste' identifies this.
    def perfect_materials(self, item):
        typeid = item['typeID']
        item['perfectMaterials'] = []
        materials = get_all(g_perfect_materials['sql'], (typeid, typeid, typeid))

        # This dict will be used to keep track of which materials have been seen. If a material
        # is listed in the regular list (affected by ME waste) and it appears in the extra
        # material list (not affected by ME waste), it must have PE waste applied to it.
        # This also requires the result set from the materials query to be sorted with normal
        # materials first followed by extra materials.
        requiredMaterials = dict()

        for material in materials:
            if material[g_perfect_materials['quantity']] > 0:
                typeid = material[g_perfect_materials['typeID']]
                wasteME = bool(material[g_perfect_materials['waste']])

                # PE always applies if ME waste applies.
                wastePE = wasteME

                if typeid in requiredMaterials:
                    wastePE = True
                else:
                    requiredMaterials[typeid] = True

                pm = {
                    'typeID': typeid,
                    'quantity': float(material[g_perfect_materials['quantity']]),
                    'dmg': float(material[g_perfect_materials['dmg']]),
                    'wasteME': wasteME,
                    'wastePE': wastePE
                }

                if self.names:
                    pm['name'] = material[g_perfect_materials['name']]

                item['perfectMaterials'].append(pm)

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
                'categoryName': item_row[g_item['categoryName']],
            }

            if self.t1bpo:
                item_row = get_one(g_t1bpo['sql'], (typeid))
                self.items[typeid]['t1bpo'] = {
                    'typeID': item_row[g_t1bpo['typeID']],
                    'blueprintTypeID': item_row[g_t1bpo['blueprintTypeID']],
                    'researchCopyTime': item_row[g_t1bpo['researchCopyTime']],
                }

                if self.names:
                    self.items[typeid]['t1bpo']['typeName'] = item_row[g_t1bpo['typeName']]

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
select invTypes.typeID, typeName, productionTime, productivityModifier, wasteFactor, maxProductionLimit, chance, categoryName
from invTypes, invBlueprintTypes, inventionChance, invGroups, invCategories
where invTypes.typeID = invBlueprintTypes.productTypeID
    and invTypes.groupID = invGroups.groupID
    and invGroups.categoryID = invCategories.categoryID
    and inventionChance.typeID = invTypes.typeID
    and invTypes.typeID = %s''',
    'typeID': 0,
    'typeName': 1,
    'productionTime': 2,
    'productivityModifier': 3,
    'wasteFactor': 4,
    'maxProductionLimit': 5,
    'chance': 6,
    'categoryName': 7
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

# Query to retrieve all inventable items except rigs.
g_inventable_no_rigs = {
    'sql': '''
select invTypes.typeID, invTypes.typeName, invGroups.categoryID
from invTypes, invMetaTypes, invGroups
where invTypes.typeID=invMetaTypes.typeID
    and invMetaTypes.metaGroupId=2
    and invGroups.groupID=invTypes.groupID
    and invTypes.published=1
    and invGroups.groupName not like "%%rig%%"
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

# Query to retrieve the datacores required. Expects one inventable item ID.
g_datacores = {
    'sql': '''
select it2.typeid,it2.typename,quantity
from invTypes,invGroups,invMetaTypes,ramTypeRequirements,invBlueprintTypes,invTypes it2
where invTypes.typeid=invMetaTypes.typeid and invMetaTypes.metaGroupId=2 and invGroups.groupid=invTypes.groupid and invBlueprintTypes.blueprintTypeID=ramTypeRequirements.typeid and invBlueprintTypes.productTypeID=invMetaTypes.parenttypeid and it2.typeid=requiredTypeID and activityID=8 and it2.groupID!=716 and invTypes.typeid=%s''',
    'typeID': 0,
    'typeName': 1,
    'quantity': 2
}

# Query to retrieve the parent T1 blueprint information. Expects one inventable item ID.
g_t1bpo = {
    'sql': '''
select t3.typeID, t3.typeName, t1.blueprintTypeID, t1.researchCopyTime
from invBlueprintTypes t1
inner join invMetaTypes t2
  on t1.productTypeID = t2.parentTypeID
inner join invTypes t3
  on t3.typeID = t1.productTypeID
where t2.typeID = %s''',
    'typeID': 0,
    'typeName': 1,
    'blueprintTypeID': 2,
    'researchCopyTime': 3
}
