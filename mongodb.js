var mapDaily = function () {
    var is_sms = this.is_sms;
    var is_incoming = is_sms && this.is_incoming;

    var data = {
        sms: is_sms ? 1 : 0,
        in: is_incoming ? 1 : 0,
        out: (is_sms && !is_incoming) ? 1 : 0
    };

    emit(Math.floor(this.start_timestamp.getTime() / 1000 / 60 / 60 / 24), data);
}

var reduce = function (key, values) {
    var result = {
        sms: 0,
        in: 0,
        out: 0,
    };

    values.forEach(function (value) {
        result.sms += value.sms;
        result.in += value.in;
        result.out += value.out;
    });

    return result;
}

db.history.mapReduce(mapDaily, reduce, {out: "daily"})

db.daily.find()

    db.history.find({"is_sms": {$exists: false}}).length()

/* today */
    Math.floor(new Date().getTime() / 1000 / 60 / 60 / 24)

    /*
{ "_id" : 15123, "value" : { "sms" : 5, "in" : 3, "out" : 2 } }
{ "_id" : 15124, "value" : { "sms" : 11, "in" : 4, "out" : 7 } }
{ "_id" : 15125, "value" : { "sms" : 0, "in" : 0, "out" : 0 } }
{ "_id" : 15126, "value" : { "sms" : 31, "in" : 15, "out" : 16 } }
{ "_id" : 15127, "value" : { "sms" : 26, "in" : 14, "out" : 12 } }
{ "_id" : 15128, "value" : { "sms" : 14, "in" : 11, "out" : 3 } }
{ "_id" : 15129, "value" : { "sms" : 0, "in" : 0, "out" : 0 } }
{ "_id" : 15130, "value" : { "sms" : 6, "in" : 4, "out" : 2 } }
{ "_id" : 15131, "value" : { "sms" : 9, "in" : 6, "out" : 3 } }
{ "_id" : 15132, "value" : { "sms" : 8, "in" : 5, "out" : 3 } }
{ "_id" : 15133, "value" : { "sms" : 9, "in" : 5, "out" : 4 } }
{ "_id" : 15134, "value" : { "sms" : 7, "in" : 3, "out" : 4 } }
{ "_id" : 15135, "value" : { "sms" : 20, "in" : 11, "out" : 9 } }
{ "_id" : 15136, "value" : { "sms" : 2, "in" : 2, "out" : 0 } }
{ "_id" : 15137, "value" : { "sms" : 0, "in" : 0, "out" : 0 } }
{ "_id" : 15138, "value" : { "sms" : 5, "in" : 3, "out" : 2 } }
{ "_id" : 15139, "value" : { "sms" : 3, "in" : 2, "out" : 1 } }
{ "_id" : 15140, "value" : { "sms" : 19, "in" : 9, "out" : 10 } }
{ "_id" : 15141, "value" : { "sms" : 2, "in" : 2, "out" : 0 } }
{ "_id" : 15142, "value" : { "sms" : 3, "in" : 1, "out" : 2 } }
{ "_id" : 15143, "value" : { "sms" : 8, "in" : 5, "out" : 3 } }
{ "_id" : 15144, "value" : { "sms" : 3, "in" : 2, "out" : 1 } }
{ "_id" : 15145, "value" : { "sms" : 11, "in" : 3, "out" : 8 } }
{ "_id" : 15146, "value" : { "sms" : 5, "in" : 2, "out" : 3 } }
{ "_id" : 15147, "value" : { "sms" : 2, "in" : 1, "out" : 1 } }
{ "_id" : 15148, "value" : { "sms" : 8, "in" : 4, "out" : 4 } }
{ "_id" : 15149, "value" : { "sms" : 6, "in" : 4, "out" : 2 } }
{ "_id" : 15150, "value" : { "sms" : 15, "in" : 8, "out" : 7 } }
{ "_id" : 15151, "value" : { "sms" : 13, "in" : 8, "out" : 5 } }
{ "_id" : 15152, "value" : { "sms" : 8, "in" : 4, "out" : 4 } }
{ "_id" : 15153, "value" : { "sms" : 2, "in" : 1, "out" : 1 } }
{ "_id" : 15154, "value" : { "sms" : 1, "in" : 1, "out" : 0 } }
{ "_id" : 15155, "value" : { "sms" : 4, "in" : 2, "out" : 2 } }
{ "_id" : 15156, "value" : { "sms" : 11, "in" : 5, "out" : 6 } }
{ "_id" : 15157, "value" : { "sms" : 11, "in" : 2, "out" : 9 } }
{ "_id" : 15158, "value" : { "sms" : 10, "in" : 3, "out" : 7 } }
{ "_id" : 15159, "value" : { "sms" : 17, "in" : 12, "out" : 5 } }
{ "_id" : 15160, "value" : { "sms" : 9, "in" : 4, "out" : 5 } }
{ "_id" : 15161, "value" : { "sms" : 4, "in" : 2, "out" : 2 } }
{ "_id" : 15162, "value" : { "sms" : 11, "in" : 5, "out" : 6 } }
{ "_id" : 15163, "value" : { "sms" : 6, "in" : 3, "out" : 3 } }
{ "_id" : 15164, "value" : { "sms" : 13, "in" : 6, "out" : 7 } }
{ "_id" : 15165, "value" : { "sms" : 10, "in" : 7, "out" : 3 } }
{ "_id" : 15166, "value" : { "sms" : 12, "in" : 3, "out" : 9 } }
{ "_id" : 15167, "value" : { "sms" : 10, "in" : 5, "out" : 5 } }
{ "_id" : 15168, "value" : { "sms" : 21, "in" : 10, "out" : 11 } }
{ "_id" : 15169, "value" : { "sms" : 13, "in" : 8, "out" : 5 } }
{ "_id" : 15170, "value" : { "sms" : 12, "in" : 4, "out" : 8 } }
{ "_id" : 15171, "value" : { "sms" : 12, "in" : 9, "out" : 3 } }
{ "_id" : 15172, "value" : { "sms" : 14, "in" : 8, "out" : 6 } }
{ "_id" : 15173, "value" : { "sms" : 15, "in" : 9, "out" : 6 } }
{ "_id" : 15174, "value" : { "sms" : 7, "in" : 4, "out" : 3 } }
{ "_id" : 15175, "value" : { "sms" : 10, "in" : 4, "out" : 6 } }
{ "_id" : 15176, "value" : { "sms" : 5, "in" : 3, "out" : 2 } }
{ "_id" : 15177, "value" : { "sms" : 3, "in" : 0, "out" : 3 } }
*/
