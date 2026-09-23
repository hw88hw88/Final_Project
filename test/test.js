const jsdom = require('jsdom');
const chai = require('chai');
const fs = require('fs');
const html_index = fs.readFileSync('./templates/index.html', 'utf-8');
const dom = new jsdom.JSDOM(
    html_index
);

global.document = dom.window.document;
global.window = dom.window;
const live_query = require('../static/script/live_query');

describe('live query', ()=>{
    describe('check variable existance', ()=>{
        it('', () => {
            const query = document.getElementById('query');
            const response = document.getElementById('response');
            const enter_button = document.getElementById('enter');
            const clear_button = document.getElementById('clear');
            const server_msg = document.getElementById('server_msg');

            chai.expect(query).to.not.be.null;
            chai.expect(response).to.not.be.null;
            chai.expect(enter_button).to.not.be.null;
            chai.expect(clear_button).to.not.be.null;
            chai.expect(server_msg).to.not.be.null;
            chai.expect(live_query.stop_timer).to.not.be.null;
            chai.expect(live_query.update_status).to.not.be.null;
            chai.expect(live_query.user_enter).to.not.be.null;
        });
    });
});