import { createRouter, createWebHistory } from "vue-router";

import MainView from "../views/MainView.vue";
import RecommendView from "../views/RecommendView.vue";
import FestivalView from "../views/FestivalView.vue";
import CommunityListView from "../views/CommunityListView.vue";
import CommunityDetailView from "../views/CommunityDetailView.vue";
import CommunityWriteView from "../views/CommunityWriteView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "main", component: MainView }, // B 담당
    { path: "/recommend", name: "recommend", component: RecommendView }, // C 담당
    { path: "/festivals", name: "festivals", component: FestivalView }, // C 담당
    { path: "/community", name: "community-list", component: CommunityListView }, // C 담당
    { path: "/community/:id", name: "community-detail", component: CommunityDetailView },
    { path: "/community/write", name: "community-write", component: CommunityWriteView },
  ],
});

export default router;
