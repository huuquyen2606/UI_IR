<template>
  <div>
    <v-row class="mx-16 mt-2" >
      <v-col cols="12">
        <v-text-field label="Search Here ..." 
            v-model="searchContent"
            clearable outlined 
            clear-icon="mdi-close-circle"
            class="mt-5" 
            append-icon='mdi-search-web'
            @click:append="searching"
        >
        </v-text-field>
      </v-col>
    </v-row>
    <v-row class='mt-1'>
      <v-col cols="8" class="ml-10 mx-5">
        <v-data-iterator
          :items="items"
          :items-per-page.sync="itemsPerPage"
          :page.sync="page"
          :search="search"
          :sort-by="sortBy.toLowerCase()"
          :sort-desc="sortDesc"
          hide-default-footer
        >
          <template v-slot:header>
            <v-toolbar
              dark
              color="blue darken-3"
              class="mb-1"
            >
              <h2 class="font-weight-bold white--text mr-5">
                List Device
              </h2>
              <v-text-field
                v-model="search"
                clearable
                flat
                solo-inverted
                hide-details
                prepend-inner-icon="mdi-magnify"
                label="Search"
              ></v-text-field>
              <template v-if="$vuetify.breakpoint.mdAndUp">
                <v-spacer></v-spacer>
                <v-select
                  v-model="sortBy"
                  flat
                  solo-inverted
                  hide-details
                  :items="keys"
                  prepend-inner-icon="mdi-magnify"
                  label="Sort by"
                ></v-select>
                <v-spacer></v-spacer>
                <v-btn-toggle
                  v-model="sortDesc"
                  mandatory
                >
                  <v-btn
                    large
                    depressed
                    color="blue"
                    :value="false"
                  >
                    <v-icon>mdi-arrow-up</v-icon>
                  </v-btn>
                  <v-btn
                    large
                    depressed
                    color="blue"
                    :value="true"
                  >
                    <v-icon>mdi-arrow-down</v-icon>
                  </v-btn>
                </v-btn-toggle>
              </template>
            </v-toolbar>
          </template>

          <template v-slot:default="props">
            <v-row>
              <v-col
                v-for="(item,index) in props.items"
                :key="item.name"
                cols="12"
                sm="6"
                md="4"
                lg="3"
              >
                <v-card>
                  <v-card-title class="subheading font-weight-bold">
                    Devices: {{ index + 1 }}
                  </v-card-title>

                  <v-divider></v-divider>

                  <v-list dense>
                    <v-list-item
                      v-for="(key, index) in filteredKeys"
                      :key="index"
                    >
                      <v-list-item-content :class="{ 'blue--text': sortBy === key }">
                        {{ key }}:
                      </v-list-item-content>
                      <v-list-item-content
                        class="align-end"
                        :class="{ 'blue--text': sortBy === key }"
                      >
                        <div class="d-flex align-center">
                          {{ item[key.toLowerCase()].toUpperCase() }}
                          <v-progress-circular class="ml-2"
                            v-if="item[key.toLowerCase()]=='training'"
                            :size="20"
                            color="primary"
                            indeterminate
                          ></v-progress-circular>
                          <v-icon class="ml-2" color="blue" aria-hidden="false" v-if="item[key.toLowerCase()]=='waiting'">
                            mdi-map-marker-radius
                          </v-icon>
                          <v-icon class="ml-2" color="orange" aria-hidden="false" v-if="item[key.toLowerCase()]=='offline'">
                            mdi-map-marker-remove
                          </v-icon>
                          <v-icon class="ml-2" color="green" aria-hidden="false" v-if="item[key.toLowerCase()]=='sent'">
                            mdi-send-check
                          </v-icon>
                        </div>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                </v-card>
              </v-col>
            </v-row>
          </template>

          <template v-slot:footer>
            <v-row
              class="mt-2"
              align="center"
              justify="center"
            >
              <span class="grey--text">Items per page</span>
              <v-menu offset-y>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    dark
                    text
                    color="primary"
                    class="ml-2"
                    v-bind="attrs"
                    v-on="on"
                  >
                    {{ itemsPerPage }}
                    <v-icon>mdi-chevron-down</v-icon>
                  </v-btn>
                </template>
                <v-list>
                  <v-list-item
                    v-for="(number, index) in itemsPerPageArray"
                    :key="index"
                    @click="updateItemsPerPage(number)"
                  >
                    <v-list-item-title>{{ number }}</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>

              <v-spacer></v-spacer>

              <span
                class="mr-4
                grey--text"
              >
                Page {{ page }} of {{ numberOfPages }}
              </span>
              <v-btn
                fab
                dark
                color="blue darken-3"
                class="mr-1"
                @click="formerPage"
              >
                <v-icon>mdi-chevron-left</v-icon>
              </v-btn>
              <v-btn
                fab
                dark
                color="blue darken-3"
                class="ml-1"
                @click="nextPage"
              >
                <v-icon>mdi-chevron-right</v-icon>
              </v-btn>
            </v-row>
          </template>
        </v-data-iterator>
      </v-col>
      <v-col cols="3" class="mx-5" >
        <v-card max-width="374" >
          <template slot="progress">
            <v-progress-linear color="deep-purple" height="10" indeterminate ></v-progress-linear>
          </template>
          <!-- <v-img height="230" src="../assets/server.jpg"></v-img> -->
          <v-card-title>Evaluating:</v-card-title>
          <v-list dense>
            <v-list-item class="blue--text">
              <v-list-item-content>
                Training Clients:
              </v-list-item-content>
              <v-list-item-content class="align-end">
                <div class="d-flex align-center">
                  {{serverContent.train}} 
                </div>
              </v-list-item-content>
            </v-list-item>
            <v-list-item class="orange--text">
              <v-list-item-content>
                Waiting Clients :
              </v-list-item-content>
              <v-list-item-content class="align-end">
                <div class="d-flex align-center">
                  {{serverContent.wait}} 
                </div>
              </v-list-item-content>
            </v-list-item>
            <v-list-item class="green--text">
              <v-list-item-content>
                Sent Models:
              </v-list-item-content>
              <v-list-item-content class="align-end">
                <div class="d-flex align-center">
                  {{serverContent.sent}} 
                </div>
              </v-list-item-content>
            </v-list-item>
            <v-list-item class="red--text">
              <v-list-item-content>
                Offline Clients:
              </v-list-item-content>
              <v-list-item-content class="align-end">
                <div class="d-flex align-center">
                  {{serverContent.off}} 
                </div>
              </v-list-item-content>
            </v-list-item>
          </v-list>
          <v-divider class="mx-3"></v-divider>
          <v-card-title>State: 
            <v-chip v-if="serverInfo.state=='aggregating'" class="text-right ml-auto white--text" color="blue">{{serverInfo.state.toUpperCase()}} </v-chip>
            <v-chip v-if="serverInfo.state=='sending'" class="text-right ml-auto white--text" color="green">{{serverInfo.state.toUpperCase()}} </v-chip>
            <v-chip v-if="serverInfo.state=='waiting'" class="text-right ml-auto white--text" color="orange">{{serverInfo.state.toUpperCase()}} </v-chip>
          </v-card-title>
          
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
  // import ListClients from "../db"
  import {db} from '../main'
  export default {
    name: 'HelloWorld',
    data: () => ({
      searchContent:'',
      serverContent : {
        'train':0,
        'off':0,
        'wait':0,
        'sent':0,
      },  
      serverInfo: {
        'numClients': 0,
        'state': 'Aggregating',
      },
      itemsPerPageArray: [4, 8, 12],
      search: '',
      filter: {},
      sortDesc: false,
      page: 1,
      itemsPerPage: 8,
      sortBy: 'id',
      keys: [
        'ID',
        'State',
      ],
      items: [
      ],
    }),
    computed: {
      numberOfPages () {
        return Math.ceil(this.items.length / this.itemsPerPage)
      },
      filteredKeys () {
        return this.keys.filter(key => key !== 'Name')
      },
    },
    methods: {
      async getEvents() {
        try {
          const ref = await db.ref('clients');
          const refSer = await db.ref('server');
          refSer.on('value',(snapshot)=>{
            this.serverInfo.state = snapshot.val().state;
          })
          ref.on('value',(snapshot)=>{
            let _items = [];
            let trainitems =0 ;
            let offitems = 0 ;
            let waititems = 0 ;
            let sentitems = 0 ;
            let list_content = snapshot.val();
            let list = Object.keys(list_content);
            list.forEach(i =>{
              if(list_content[i].state=='training'){
                trainitems +=1;
              }else if(list_content[i].state=='waiting'){
                waititems +=1;
              }else if(list_content[i].state=='offline'){
                offitems +=1;
              }else if(list_content[i].state=='sent'){
                sentitems +=1;
              }
              _items.push({id:i,state:list_content[i].state})
            })
            console.log({train:trainitems,off:offitems,wait:waititems,sent:sentitems})
            this.serverContent = {train:trainitems,off:offitems,wait:waititems,sent:sentitems};
            this.items = _items;
          })
        } catch (error) {
          console.log(error);
        }
      },
      nextPage () {
        if (this.page + 1 <= this.numberOfPages) this.page += 1
      },
      formerPage () {
        if (this.page - 1 >= 1) this.page -= 1
      },
      updateItemsPerPage (number) {
        this.itemsPerPage = number
      },
      searching(){
        this.searchContent = ''
      },
    },
    created(){
      this.getEvents();
    },
  }
</script>
