<!-- 📂 src/components/Sidebar.vue -->
<template>
    <el-aside width="250px" class="sidebar">
      <div class="sidebar-header">
        <img src="../assets/title.png" alt="Website Logo" class="sidebar-logo" />
        <h2 class="sidebar-title">Polygon Complexity System</h2>
      </div>
        <el-menu
            :default-active="activeIndex"
            :router = "true"
            :default-openeds="openSubMenus"
        >
            <el-menu-item :index="'/'" @click="updateActiveIndex('/')">
              Home
            </el-menu-item>
            <el-menu-item :index="'/systemdescription'" @click="updateActiveIndex('/systemdescription')">
              System Description
            </el-menu-item>

            <el-menu-item :index="'/system'" @click="updateActiveIndex('/system')">
              System
            </el-menu-item>
  
            <!--  Theory  -->
            <el-sub-menu 
            :index="'/theory'"
            @click="toggleTheoryMenu" 
            ref = "theorySubMenu"
            :style="{ '--theory-arrow-color': isTheoryOpen ? 'brightness(0) saturate(100%) invert(79%) sepia(47%) saturate(653%) hue-rotate(344deg) brightness(102%) contrast(102%)' : 'white' }"
            >
              <template #title> 
                <span :class="{ 'active-theory-title': isTheoryOpen }">Theory</span>
              </template>
              <el-menu-item :index="'/theory/downsampling'" @click="updateActiveIndex('/theory/downsampling')">Downsampling</el-menu-item>
              <el-menu-item :index="'/theory/boundary'" @click="updateActiveIndex('/theory/boundary')">Boundary</el-menu-item>
              <el-menu-item :index="'/theory/triangulation'" @click="updateActiveIndex('/theory/triangulation')">Triangulation</el-menu-item>
              <el-menu-item :index="'/theory/entropy'" @click="updateActiveIndex('/theory/entropy')">Entropy</el-menu-item>
              <el-menu-item :index="'/theory/skeleton'" @click="updateActiveIndex('/theory/skeleton')">Skeleton</el-menu-item>
              <el-menu-item :index="'/theory/weighted'" @click="updateActiveIndex('/theory/weighted')">Weighted</el-menu-item>
            </el-sub-menu>
  
            <el-menu-item :index="'/about'" @click="updateActiveIndex('/about')">
              About Us
            </el-menu-item>
        </el-menu>
    </el-aside>
</template>
  
<script>
  export default {
    name: "Sidebar",
    data() {
      return {
        activeIndex: this.$route.path,
        openSubMenus: ["/theory"],
        isTheoryOpen: true,
      };
    },

    watch: {
        $route(to) {
            this.activeIndex = this.getActiveIndex(to.path); 

            if (to.path.startsWith('/theory')) {
                if (!this.openSubMenus.includes('/theory')) {
                    this.openSubMenus = ['/theory'];
                }
            } 
        }
    },

    methods: {
      getActiveIndex(path) {
        if (path.startsWith("/Select") || path.startsWith("/Upload") || path.startsWith('/Draw')) {
          return "/system"; // 让 "System" 选项保持选中
        }
        return path; // 否则使用默认路径
      },

        updateActiveIndex(path) {
            this.activeIndex = path; 
            this.$router.push(path);
            //console.log(this.activeIndex);

            if (path.startsWith('/theory') && !this.openSubMenus.includes('/theory')) {
                this.openSubMenus = ['/theory'];
                    
            }
            //console.log(this.openSubMenus);
        },

        toggleTheoryMenu(event) {
            const clickedElement = event.target;
            const theoryTitle = this.$refs.theorySubMenu.$el.querySelector('.el-sub-menu__title');
            if (clickedElement === theoryTitle || theoryTitle.contains(clickedElement)) {
                this.isTheoryOpen = !this.isTheoryOpen;
            }

            if (this.isTheoryOpen) {
                this.openSubMenus = ['/theory']; 
                //console.log(this.openSubMenus);
            } 
            else {
                this.openSubMenus = this.openSubMenus.filter(i => i !== "theory"); 
            }
        },
    }
  };
</script>
  
<style scoped>
  /* 侧边栏样式 */
.sidebar {
    background-color: white;
    min-height: 100vh;
    width: 270px;
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
    overflow: hidden;
    border: 2px solid #FFD992; 
}

.sidebar-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #ffd992; 
  padding: 20px;
}

.sidebar-logo {
  width: 130px; 
  height: 130px;
  /*border-radius: 50%;*/ 
  object-fit: cover;
}

.sidebar-title {
  font-size: 23px;
  font-weight: bold;
  color: rgb(100, 53, 0); 
  margin-top: 10px;
  text-align: center;
}
  
.el-menu {
    font-size: 18px;
    transform: none;
    background-color: white;
    box-sizing: border-box;
    overflow: hidden;
    width: 100%;
    height: 100%;
}
  
.el-menu-item {
    font-size: 18px;
    background-color: white;
    color: rgb(100, 53, 0);
    width: 100%;
    max-width: 270px; 
    padding: 0 15px;
    box-sizing: border-box;
}
  
:deep(.el-sub-menu__title) {
    font-size: 18px;
    background-color: white;
    color: rgb(128, 68, 0);
}

:deep(.el-sub-menu) {
  width: 100%;
  max-width: 270px; 
  box-sizing: border-box;
}

:deep(.active-theory-title) { 
    color: #ffd992 ;
}

.el-menu-item.is-active {
    background-color: #ffd992; 
    color: white;
    font-weight: bold;
    border: 2px solid white;

}

:deep(.el-sub-menu__title .el-sub-menu__icon-arrow) {
  filter: var(--theory-arrow-color);
  transition: color 0.3s ease-in-out
}

.el-menu-item:hover,
:deep(.el-sub-menu__title:hover) {
    background-color: #d9f1ee; 
    transition: color 0.3s ease-in-out
}

:deep(.el-menu--popup-container) {
    max-width: 270px;
    overflow: hidden;
}
</style>
  