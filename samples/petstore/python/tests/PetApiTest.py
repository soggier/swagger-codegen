#!/usr/bin/env python

import sys
import unittest
import urllib2
import json
import random

from BaseApiTest import BaseApiTest

sys.path = ['./'] + sys.path
from petstore import *
from petstore.models import *


class PetApiTest(BaseApiTest):

    @classmethod
    def setUpClass(cls):
        # super(PetApiTest, self).setUp()
        cls.randomId = long(int(90000 * random.random()) + 10000)

    def testPetApis(self):
        response = urllib2.urlopen(self.apiUrl + '/pet.json')
        doc = json.loads(response.read())
        assert len(doc['apis']) == 3, 'there should be 3 pet apis'

    def testPetApisAuthenticated(self):
        response = urllib2.urlopen(self.apiUrl + '/pet.json?' +
                                   'api_key=special-key')
        doc = json.loads(response.read())
        assert len(doc['apis']) == 4, 'there should be 4 pet apis when' + \
                                      'authenticated'

    def testGetPetById(self):
        res = self.petApi.getPetById(1)
        assert res, 'null getWord result'
        assert res.id == 1, 'pet id should be 1'

    def testAddPet(self):
        pet = Pet.Pet()

        pet.id = self.randomId
        tag1 = Tag.Tag()
        tag1.name = "tag1"
        tag2 = Tag.Tag()
        tag2.name = "some tag"
        pet.tags = [tag1, tag2]
        category = Category.Category()
        category.name = "Cats"
        pet.category = category
        pet.status = "sold"
        pet.name = "Shermie"
        pet.photoUrls = ["http://foo.com/1.jpg", "http://foo.com/1.jpg"]
        self.petApi.addPet(pet)

        new_pet = self.petApi.getPetById(pet.id)

        assert new_pet.id == pet.id, 'ids should match'
        assert new_pet.name == pet.name, 'names should match'
        assert(set([tag.name for tag in new_pet.tags]) ==
               set([tag.name for tag in pet.tags])), 'tags should match'
        assert new_pet.status == pet.status, 'status should match'
        assert new_pet.category.name == pet.category.name, 'category should match'
        assert new_pet.photoUrls == pet.photoUrls, 'photoUrls should match'

    def testUpdatePet(self):
        alpahbet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

        pet = Pet.Pet()
        pet.id = self.randomId

        tag1 = Tag.Tag()
        tag1.name = "special-tag"
        tag2 = Tag.Tag()
        random.shuffle(alpahbet)
        tag2.name = ''.join(alpahbet)
        pet.tags = [tag1, tag2]
        category = Category.Category()
        random.shuffle(alpahbet)
        category.name = ''.join(alpahbet)
        pet.category = category
        pet.status = "sold"
        random.shuffle(alpahbet)
        pet.name = ''.join(alpahbet)
        pet.photoUrls = ["http://foo.com/22.jpg", "http://foo.com/55.jpg"]
        self.petApi.updatePet(pet)

        updated_pet = self.petApi.getPetById(pet.id)

        assert updated_pet.id == pet.id, 'ids should match'
        assert updated_pet.name == pet.name, 'names should match'
        assert(set([tag.name for tag in updated_pet.tags]) ==
               set([tag.name for tag in pet.tags])), 'tags should match'
        assert updated_pet.status == pet.status, 'status should match'
        assert updated_pet.category.name == pet.category.name, 'category should match'
        assert updated_pet.photoUrls == pet.photoUrls, 'photoUrls should match'

    def testFindPetsByTags(self):
        pet = Pet.Pet()
        pet.id = self.randomId

        tag1 = Tag.Tag()
        tag1.name = "special-tag"
        pet.tags = [tag1]
        self.petApi.updatePet(pet)

        res = self.petApi.findPetsByTags("special-tag")
        assert self.randomId in [pet.id for pet in res], 'must find by tag'

    def testFindPetsByStatus(self):
        pet = Pet.Pet()
        pet.id = self.randomId

        tag1 = Tag.Tag()
        tag1.name = "special-tag"
        pet.status = "sold"
        self.petApi.updatePet(pet)

        res = self.petApi.findPetsByStatus("sold")
        assert self.randomId in [pet.id for pet in res], 'must find by status'

    # def testGetWordWithCanonicalForm(self):
    #     res = self.wordApi.getWord('cAt', useCanonical=True)
    #     assert res, 'null getWord result'
    #     assert res.word == 'cat', 'word should be "cAt"'

    # def testGetDefinitions(self):
    #     res = self.wordApi.getDefinitions('cat', limit=10)
    #     assert res, 'null getDefinitions result'
    #     assert len(res) == 10, 'should have 10 definitions'

    # def testGetExamples(self):
    #     res = self.wordApi.getExamples('cat', limit=5)
    #     assert res, 'null getExamples result'
    #     assert len(res.examples) == 5, 'should have 5 definitions'

    # def testGetTopExample(self):
    #     res = self.wordApi.getTopExample('cat')
    #     assert res, 'null getTopExample result'
    #     assert res.word == 'cat', 'word should be "cat"'

    # # def testGetTextPronunciations(self):
    # #     res = self.wordApi.getTextPronunciations('cat')
    # #     assert res, 'null getTextPronunciations result'
    # #     assert len(res) == 2, 'should have 2 prons for "cat"'

    # def testGetHyphenation(self):
    #     res = self.wordApi.getHyphenation('catalog', limit=1)
    #     assert res, 'null getHyphenation result'
    #     assert len(res) == 1, 'hypenation length should be 1'

    # def testGetWordFrequency(self):
    #     res = self.wordApi.getWordFrequency('cat')
    #     assert res, 'null getWordFrequency result'
    #     assert res.totalCount != 0, 'total count should not be 0'

    # def testGetPhrases(self):
    #     res = self.wordApi.getPhrases('money')
    #     assert res, 'null getPhrases result'
    #     assert len(res) != 0, 'getPhrases length should not be 0'

    # def testGetRelatedWords(self):
    #     res = self.wordApi.getRelatedWords('cat')
    #     assert res, 'null getRelatedWords result'
    #     for related in res:
    #         assert len(related.words) <= 10, 'should have <= 10 related words'

    # def testGetAudio(self):
    #     res = self.wordApi.getAudio('cat', useCanonical=True, limit=2)
    #     assert res, 'null getAudio result'
    #     assert len(res) == 2, 'getAudio size should be 2'


if __name__ == "__main__":
    unittest.main()
