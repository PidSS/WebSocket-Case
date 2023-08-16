<script lang="ts">;
export default {
    data():{
        messages: { source?:string, message:string, type?:string }[],
        ws: WebSocket,
        inputing: string
    } {
        return {
            messages: [],
            ws: new WebSocket(this.wsServer),
            inputing: ""
        }
    },

    props: {
        wsServer: { type: String, required: true }
    },

    methods: {
        appendMessage(source:string, message:string) {
            this.messages.push({
                source: source,
                message: message
            });
        },

        submitInput() {
            let data = this.inputing
            if (data!=="") {
                this.appendMessage("client", data);
                this.ws.send(data);
            }
            this.inputing = "";
        }
    },

    created() {
        // const ws = new WebSocket(this.wsserver);
        this.ws.onopen = ()=> {
            this.messages.push({
                type: "info",
                message: "连接已建立"
            })
        }

        this.ws.onclose = ()=> {
            this.messages.push({
                type: "info",
                message: "连接已断开"
            })
        }

        this.ws.onerror = (event)=> {
            alert("WebSocket发生错误");
            console.error(event);
        }
        this.ws.onmessage = (ev)=> {
            this.appendMessage("server", ev.data);
        }
    },

    computed: {
        msgFitAbove() {
            return (index:number)=> {
                return index>0 && this.messages[index-1].source===this.messages[index].source;
            }
        },
        msgFitBelow() {
            return (index:number)=> {
                return index+1<this.messages.length && this.messages[index+1].source===this.messages[index].source;
            }
        }
    }
}
</script>

<template>
    <div id="Console">
        <div class="title">会话</div>
        <div class="devideLine"></div>
        <div class="scroll">
            <div v-for="(item, index) in messages">
                <div v-if="item.type==='info'" class="info">{{ item.message }}</div>
                <div v-else class="bubble"
                :class="{
                    self: item.source==='client',
                    fitAbove: msgFitAbove(index),
                    fitBelow: msgFitBelow(index)
                }">
                    {{ item.message }}
                </div>
            </div>
        </div>
        <div class="devideLine"></div>
        <div class="input">
            <input v-model="inputing" @keyup.enter="submitInput">
            <button @click="submitInput">发送</button>
        </div>
    </div>
</template>

<style>
#Console {
    background-color: var(--vt-c-black-mute);
    padding: 18px 5% 24px;
    border-radius: 18px;
    display: flex;
    flex-flow: column nowrap;
    align-items: center;
}

.title {
    flex: none;
    height: 36px;
    line-height: 36px;
    color: var(--vt-c-white-soft);
    font-size: 20px;
    font-weight: bold;
}

.scroll {
    position: relative;
    padding: 0 7%;
    display: flex;
    flex-flow: column;
    overflow-x: hidden;
    overflow-y: auto;
    scrollbar-width: none;
    width: 100%;
}

::-webkit-scrollbar {
display: none; /* Chrome Safari */
}

.info {
    margin: auto;
    width: fit-content;
    background-color: #f2f2f214;
    color: var(--vt-c-text-dark-2);
    font-size: 12px;
    padding: 2px 8px;
    border-radius: 10px;
    opacity: 0.8;
}

.bubble {
    position: relative;
    width: fit-content;
    max-width: 85%;
    padding: 10px 12px;
    margin: 14px 0;
    border-radius: 8px;
    line-height: 16px;
    background-color: var(--vt-c-white-mute);
    color: var(--vt-c-black-mute);
    font-weight: bold;
    font-size: 14px;
    overflow: hidden;
    word-wrap:break-word;
}

.self {
    float: right;
    background-color: var(--vt-c-theme);
    color: var(--vt-c-white-mute);
}

.bubble:is(.self).fitAbove {
    margin-top: 1.2px;
    border-top-right-radius: 1px;
}

.bubble:is(.self).fitBelow {
    margin-bottom: 1.2px;
    border-bottom-right-radius: 1px;
}

.bubble:not(.self).fitAbove {
    margin-top: 1.2px;
    border-top-left-radius: 1px;
}

.bubble:not(.self).fitBelow {
    margin-bottom: 1.2px;
    border-bottom-left-radius: 1px;
}

.scroll {
    flex: auto;
}

.input {
    flex: none;
    height: 32px;
    width: 100%;
    display: flex;
    flex-flow: row nowrap;
    justify-content: space-between;
    font-weight: bold;
    font-size: 16px;
}

.input input {
    box-sizing: border-box;
    border: 2px transparent;
    outline: 2px solid #f2f2f214;
    outline-color: transparent;
    background-color: #f2f2f214;
    width: 100%;
    margin-right: 12px;
    padding: 0 16px;
    border-radius: 10px;
    transition: outline-color 0.1s;
    color: var(--vt-c-white-mute);
    font: inherit;
}

.input input:focus {
    outline: 2px solid var(--vt-c-theme);
}

.input button {
    width: 80px;
    border: none;
    background-color: var(--vt-c-theme);
    border-radius: 6px;
    color: var(--vt-c-white-soft);
    box-shadow: inset 0 0 0 50vmax transparent;
    transition: box-shadow 0.1s;
    font: inherit;
}

.input button:hover {
    box-shadow: inset 0 0 0 50vmax rgba(255, 255, 255, 0.2);
}

.input button:active {
    box-shadow: inset 0 0 0 50vmax rgba(255, 255, 255, 0.35);
}

.devideLine {
    flex: none;
    width: 100%;
    height: 2px;
    margin: 16px 0;
    /* opacity: 60%; */
    background-color: var(--vt-c-divider-dark-1);
}
</style>