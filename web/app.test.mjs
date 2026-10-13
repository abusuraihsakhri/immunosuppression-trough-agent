import {test} from "node:test";
import assert from "node:assert/strict";
import {evaluate} from "./app.mjs";

const base = {task_id:"DEMO-1",target_identifier:"SPEC-1",primary_metric:10,secondary_metric:5,status_descriptor:"NORMAL",is_critical_flag:false};
test("normal demonstration",()=>{const out=evaluate(base);assert.equal(out.overall_urgency,"ROUTINE");assert.equal(out.total_alerts,0)});
test("high metrics trigger both demo rules",()=>{const out=evaluate({...base,primary_metric:26,secondary_metric:13});assert.equal(out.overall_urgency,"ELEVATED_RISK");assert.equal(out.total_alerts,2)});
test("critical flag always dominates",()=>{const out=evaluate({...base,is_critical_flag:true});assert.equal(out.overall_urgency,"CRITICAL_STAT_PANIC");assert.equal(out.total_alerts,1)});
test("status keywords yield an alert",()=>{assert.equal(evaluate({...base,status_descriptor:"DISCORDANT_ANOMALY"}).total_alerts,1)});
test("reject invalid inputs",()=>{for(const metric of [NaN,Infinity,-1])assert.throws(()=>evaluate({...base,primary_metric:metric}));assert.throws(()=>evaluate({...base,task_id:"patient name"}));assert.throws(()=>evaluate({...base,is_critical_flag:"false"}))});
