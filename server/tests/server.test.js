const expect = require('expect');
const request = require('supertest');

const {app} = require('./../server');
const {Citation} = require('./../models/citation');