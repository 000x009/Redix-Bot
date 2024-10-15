const {Telegraf} = require('telegraf');
const bot = new Telegraf('7371925468:AAHx7Drjuy2xQI3m6qJNbyW-sTX8h1sk5-U');
const web_link = 'https://ireserve.kz/';
bot.start((ctx) => {
    console.log(ctx.from.id);
        ctx.reply('Welcome', {
            reply_markup: {
                keyboard: [
                    [{
                        text: 'open shop', web_app: {
                            url: web_link

                        }
                    }]
                ]
            }
        })
    }
)
bot.launch();