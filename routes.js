var request = require('request');
const fs = require('fs');
var path = require("path");
var express = require('express');
var dbHelper = require('./db-helper');

module.exports = function(app) {

    app.use(express.static('public'));

    app.get('/home', function(req, res){

        //get links from db
        dbHelper.getHomePageLinks('trending', function(err, data){
            if(err){
                console.log('some error!!');
                res.render('home.ejs', {'homePageContent': 'hahahahahaha'})

            }else{
                res.render('home.ejs', {'homePageContent': JSON.stringify(data)})
            }
        });
    });

    app.get('/page/:link', function(req, res){

        var linkTitle = req.params.link;
        console.log('link title -->' +linkTitle)

        res.render(linkTitle + ".ejs")

    });

    app.get('/login-page', function(req, res){

        var action = req.query.action;
        console.log('action-->' +action)

        res.render('login.ejs', {'action': action})

    });

    app.post('/login', function(req, res){

        var userid = req.body.userid;
        dbHelper.isUserVerified(userid, function(err, data){

            if(err){
                console.log('some error!!');
            }else{

                res.json({'isverified': true})
            }

        })

    });

    app.get('/users/id/:userid', function(req, res){
        var userid = req.params.userid;

        console.log('user id -->' +userid);
        try{
            userid = parseInt(userid);

             //get user info from database
            dbHelper.getUserInfo(userid, function(err, data){

            if(err){
                console.log('some error!!');
            }else{
                console.log('user data-->' +JSON.stringify(data))
                res.render('profile.ejs', {'userinfo': data})        
            }
         });
        }catch(err){
            console.log(err)
            res.json({'response': 'empty'})  
        }
        
    });

}