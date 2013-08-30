import aaf
import aaf.mob
import aaf.metadef
import aaf.iterator

import unittest
import traceback

import os


cur_dir = os.path.dirname(os.path.abspath(__file__))

sandbox = os.path.join(cur_dir,'sandbox')
if not os.path.exists(sandbox):
    os.makedirs(sandbox)

main_test_file = os.path.join(cur_dir,"files/test_file_01.aaf")
print main_test_file
assert os.path.exists(main_test_file)

class TestFile(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_new_file_aaf(self):
        test_file = os.path.join(sandbox,"new_file.aaf")
        f = aaf.open(test_file, 'w')
        f.save()
        
    def test_save_as_aaf(self):
        test_file = main_test_file
        copy_file = os.path.join(sandbox,"copy_file.aaf")
        f = aaf.open(test_file)
        
        new = f.save(copy_file)
        
    def test_new_file_xml(self):
        test_file = os.path.join(sandbox,"new_file.xml")
        f = aaf.open(test_file, 'w')
        
        f.save()
        
    def test_save_as_xml(self):
        test_file = main_test_file
        copy_file = os.path.join(sandbox,"copy_file.xml")
        f = aaf.open(test_file)
        
        new = f.save(copy_file)

        
    def test_file_modify(self):
        test_file = os.path.join(sandbox,"modify_file.aaf")
        f = aaf.open(test_file, 'w')
        f.save()
        f.close()
        
        f = aaf.open(test_file, 'rw')
        
        f.save()
        
    def test_file_readonly(self):
        test_file = os.path.join(sandbox,"readonly_file.aaf")
        f = aaf.open(test_file, 'w')
        f.save()
        f.close()
        
        f = aaf.open(test_file, 'r')
        f.save()
        
    def test_file_transient(self):
        
        output_file =  os.path.join(sandbox,"transient_output.aaf")
        f = aaf.open(None, 't')
        f.save() # Doesn't do anything but should crash
        f.save(output_file)
        f.close()
        
    def test_master_mobs(self):
        
        test_file = main_test_file
        
        f = aaf.open(test_file)
    
        header = f.header()
        
        dictionary = header.dictionary()
        storage = header.storage()
        
        print storage.count_mobs()
        
        for mob in storage.master_mobs():
            mob.count_properties()
            masterMob = aaf.mob.MasterMob(mob)
            masterMob.count_properties()
            #print "*master", masterMob
            #print "*master name", masterMob.name
            reg_mob = aaf.mob.Mob(masterMob)
            #print "converted back", reg_mob,reg_mob.name

    def test_comp_mobs(self):
        
        test_file = main_test_file
        
        f = aaf.open(test_file)
    
        header = f.header()
        
        dictionary = header.dictionary()
        storage = header.storage()
        
        #print storage.count_mobs()
        
        for mob in storage.composition_mobs():
            mob.count_properties()
            compMob = aaf.mob.CompositionMob(mob)
            #print "*compMob", compMob
            #print "*compMob name", compMob.name
            reg_mob = aaf.mob.Mob(compMob)
            #print "converted back", reg_mob,reg_mob.name
            
    def test_toplevel_mobs(self):
        
        test_file = main_test_file
        
        f = aaf.open(test_file)
    
        header = f.header()
        
        dictionary = header.dictionary()
        storage = header.storage()
        
        print storage.count_mobs()
        
        for mob in storage.toplevel_mobs():
            compMob = aaf.mob.CompositionMob(mob)
            definition = compMob.definition()
            print definition, definition.name
            print "*compMob", compMob, compMob.count_properties()
            print "*compMob name", compMob.name
            reg_mob = aaf.mob.Mob(compMob)
            print "converted back", reg_mob,reg_mob.name,reg_mob.count_properties(), reg_mob.definition().name
    
    def test_file_properties(self):
        test_file = main_test_file
        
        f = aaf.open(test_file)
        
        #for p in f.properties():
            #print p.name, p.value_typedef(),p.property_def(), p.value
            
    def test_header(self):
        test_file = main_test_file
        
        f = aaf.open(test_file)
    
        header = f.header()
        
        for p in header.properties():
            pass
            #print p.name, p.value_typedef(),p.property_def(), p.value
            
            
    def test_storage(self):
        test_file = main_test_file
        
        f = aaf.open(test_file)
    
        header = f.header()
        
        dictionary = header.dictionary()
        storage = header.storage()
        
        for p in storage.properties():
            pass
            value_typedef = p.value_typedef()
            
            value =  p.value
            print p.name, value_typedef, value_typedef.category,p.property_def()
            
            if isinstance(value, aaf.iterator.BaseIterator):
                for item in value:
                    pass
                    #print "wee",item.value
            
    def test_dictionary(self):
        test_file = main_test_file
        
        f = aaf.open(test_file)
    
        header = f.header()
        
        dictionary = header.dictionary()
        storage = header.storage()
        
        for p in dictionary.properties():
            pass
            #print p.name, p.value_typedef(),p.property_def(), p.value
        
        
    def test_properties(self):
        test_file = main_test_file
        
        f = aaf.open(test_file)
    
        header = f.header()
        
        dictionary = header.dictionary()
        storage = header.storage()
        
        print storage.count_mobs()
        
        for mob in storage.mobs():
            #print mob.count_properties()
            for p in mob.properties():
                value = p.property_value()
                valuedef = value.typedef()
                
                if valuedef.value(value) is None:
                    #pass
                    print valuedef,valuedef.category
                #print valuedef
                #print p,valuedef.name,
                #print valuedef.category
                if valuedef.category == 1:
                    intDef = aaf.metadef.TypeDefInt(valuedef)
                    size = intDef.size()
                    signed = intDef.is_signed()
                    v = intDef.value(value)
                   # print v,size
                    
                if valuedef.category == 3:
                    strongRef = aaf.metadef.TypeDefStrongObjRef(valuedef)
                    obj = strongRef.value(value)
                    obj_type = strongRef.object_type()
                    #print strongRef
                    #print strongRef.value(value),strongRef.object_type().name
                    
                if valuedef.category == 6:
                    enum = aaf.metadef.TypeDefEnum(valuedef)
                    element_typdef = enum.element_typedef()
                    value = enum.value(value)
                      
                    
                if valuedef.category == 7:
                    VariableArrayDef = aaf.metadef.TypeDefFixedArray(valuedef)
                    
                    count = VariableArrayDef.count(value)
                    typedef = VariableArrayDef.type()
                    #print VariableArrayDef.count(value), VariableArrayDef,VariableArrayDef.name,typedef.name
                    for item in VariableArrayDef.value(value):
                        name = item.typedef().name
                        #rint '  ', item, name
                    
                if valuedef.category == 8:
                    VariableArrayDef = aaf.metadef.TypeDefVariableArray(valuedef)
                    
                    size = VariableArrayDef.size(value)
                    typedef = VariableArrayDef.type()
                    #print VariableArrayDef.count(value), VariableArrayDef,VariableArrayDef.name,typedef.name
                    for item in VariableArrayDef.value(value):
                        name = item.typedef().name
                        #print '  ', item, name
                    #print '   ', p.name, intDef,signed, '=',v
                
                if valuedef.category == 10:
                    recordDef = aaf.metadef.TypeDefRecord(valuedef)
                    #print '   ',p.name, recordDef, recordDef.value(value)
                    #print p.name
                    for x in xrange(recordDef.size()):
                        member_name = recordDef.member_name(x)
                        member_type = recordDef.member_type(x)
                        
                    record_value = recordDef.value(value)
                    for key,value in record_value.items():
                        pass
                        #print '   ', key,value
                        #print '      ',recordDef.member_name(x),recordDef.member_type(x).name
                if valuedef.category == 12:
                    stringDef = aaf.metadef.TypeDefString(valuedef)
                    
                if valuedef.category == 13:
                    enumExDef = aaf.metadef.TypeDefExtEnum(valuedef)
                    size = enumExDef.size()
                    #print size ,enumExDef
                    for key,value in enumExDef.value(value).items():
                        pass
                        #print key,'=', value
                    
                    #for i in xrange(size):
                        #print enumExDef.element_name(i)
                    #print '   ',p.name, stringDef.value(value)
                #print p, p.definition().name, value, value.typedef().name, value.typedef().category
        
                

if __name__ == '__main__':
    unittest.main()