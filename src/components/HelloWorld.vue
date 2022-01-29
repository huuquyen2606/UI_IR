<template>
  <div>
    <v-card-subtitle
      elevation="10"
      outlined
      shaped
      class="mx-16 mt-2"
    >
      QTP Search is a website that helps to search for articles related to health topics.
      The source is articles taken from 3 reliable online newspapers including VnExpress, Thanh Nien and Dan Tri.
      And these articles were written from January 2021 to December 2021.
      Executing members include Nguyen Huu Quyen - 18521321, Nguyen Tan Phuc - 18521259 and Hoang Ngoc Ba Thi - 19522255.
      And most importantly, this search system only supports searching in Vietnamese
      <div>Suggested keywords: 'Covid19', 'NCOV', 'ung thư', 'vaccine', 'tiêm phòng mũi 3' ...</div>
    </v-card-subtitle>
    <v-row class="mx-16" >
      <v-col cols="12">
        <v-text-field label="Search Here ..." 
            v-model="searchContent"
            outlined 
            clear-icon="mdi-close-circle"
            :clearable = "!loading"
            append-icon='mdi-search-web'
            @click:append="searching"
            @keydown.enter="searching"
            :loading="loading"
        >
        </v-text-field>
      </v-col>
    </v-row>
    <v-row  v-if="items.length>0">
      <v-col cols="11" class="mx-16">
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
                List Documents
              </h2>
              <template v-if="$vuetify.breakpoint.mdAndUp">
                <v-spacer></v-spacer>
                <v-select
                  v-model="sortBy"
                  flat
                  solo-inverted
                  hide-details
                  :items="keys"
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
                v-for="item in props.items"
                :key="item.id"
                cols="12"
                lg="6"
              >
                <v-card>
                  <v-card-title class="subheading font-weight-bold">
                    <!-- Doc {{ item.id}} -->
                    <v-btn text x-large @click="newSite(item.link)"  >
                      Doc {{item.id}}
                      <v-icon color="blue" class="ml-2">
                        mdi-page-next-outline
                      </v-icon>
                    </v-btn>
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
                          {{ item[key.toLowerCase()]}}
                        </div>
                      </v-list-item-content>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-content :class="{ 'blue--text': sortBy === 'Ref' }">
                        Ref:
                      </v-list-item-content>
                      <v-list-item-content
                        class="align-end"
                        :class="{ 'blue--text': sortBy === 'Ref' }"
                      >
                        <div class="d-flex align-center">
                          {{item['ref'] == 1 ? 'VnExpress' : item['ref'] == 2 ? 'Dân Trí':'Thanh Niên'}}
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
    </v-row>
  </div>
</template>

<script>
  // import {db} from '../main'
  import axios from 'axios';
  export default {
    name: 'HelloWorld',
    data: () => ({
      searchContent:'',
      itemsPerPageArray: [4, 8, 12],
      search: '',
      filter: {},
      sortDesc: true,
      loading: false,
      page: 1,
      itemsPerPage: 4 ,
      sortBy: 'cosi',
      keys: [
        'ID',
        'Cosi',
        'Ref',
      ],
      items: [
      ],
      docs: [
      ],
    }),
    computed: {
      numberOfPages () {
        return Math.ceil(this.items.length / this.itemsPerPage)
      },
      filteredKeys () {
        return this.keys.filter(key => key !== 'Ref' && key !== 'Link')
      },
    },
    methods: {
      onGet(que) {
        try {
          axios.get(
            "https://huuquyenir.vync.online/query/"+que
          ).then(response =>{
            // JSON responses are automatically parsed.
            console.log(response.data);
            // let _docs = [];
            response.data.forEach(i=>{
              console.log(i)
            })
            this.items = response.data;
            this.loading = false;
          })
          
        } catch (error) {
          console.log(error);
        }
      },
      newSite(link){
        window.open(link, "_blank");    
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
        if(this.searchContent!=''){
          this.loading = true;
          this.onGet(this.searchContent);
        }
      },
    },
    // created(){
    //   this.getEvents();
    // },
  }
</script>
